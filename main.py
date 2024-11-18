import os
import shutil

from tqdm import tqdm

from modules.file_utils import create_output_directories, list_files_in_directory
from modules.face_recognition_utils import load_encodings_for_each_person, contains_face
from modules.image_classification import is_nature_image, is_non_photo
from modules.video_classification import extract_frames_from_video

image_valid_extensions = {'.png', '.jpg', '.jpeg', '.bmp', '.gif'}
video_valid_extensions = {'.mp4', '.avi', '.mov', '.mkv'}

def process_image(file_path, people_encodings):
    try:
        for person_name, encodings in people_encodings.items():
            if contains_face(file_path, encodings):
                return person_name
            
        # Check if the image contains a face
        if contains_face(file_path, None):
            return "anonymous"

        if is_nature_image(file_path):
            return "nature"

        if is_non_photo(file_path):
            return "others"
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

def detect_person_in_video(video_path, people_encodings, frame_interval=30):
    frames = extract_frames_from_video(video_path, frame_interval)
    for frame in frames:
        for person_name, encodings in people_encodings.items():
            if contains_face(frame, encodings):
                return person_name
    return None

def get_all_people_subdirectories(source_folder):
    subfolders = sorted(
        [os.path.join(source_folder, folder) for folder in os.listdir(source_folder) if os.path.isdir(os.path.join(source_folder, folder))],
        key=lambda x: int(x.split('.')[0]) if x.split('.')[0].isdigit() else float('inf')  # Sort by number prefix
    )
    return subfolders


def get_folders_to_sort(root_folder):
    """
    Retrieve all folders in the root directory that:
    - Do not end with '_sorted'
    - Are not named 'people_photos'
    """
    unsorted_folders = []
    for folder in os.listdir(root_folder):
        folder_path = os.path.join(root_folder, folder)
        if os.path.isdir(folder_path) and not folder.endswith("_sorted") and folder != "people_photos":
            unsorted_folders.append(folder_path)
    return unsorted_folders

if __name__ == "__main__":
    # Define folders
    media_root_folder = "media_root"
    reference_photos_folder = f"{media_root_folder}/people_photos"
    folders_to_sort = get_folders_to_sort(media_root_folder)
    
    for source_folder in folders_to_sort:
        output_folder = f"{source_folder}_sorted"
        create_output_directories([output_folder])

        # Encode people's face
        subfolders = get_all_people_subdirectories(reference_photos_folder)
        people_encodings = load_encodings_for_each_person(subfolders)

        # Gather all image and video files from the source folder
        image_files = list_files_in_directory(source_folder, image_valid_extensions)
        video_files = list_files_in_directory(source_folder, video_valid_extensions)
        
        # Process each image
        for image_path in tqdm(image_files):
            folder = process_image(image_path, people_encodings)
            if folder:
                os.makedirs(os.path.join(output_folder, folder), exist_ok=True)
                output_path = os.path.join(output_folder, folder, os.path.basename(image_path))
                shutil.move(image_path, output_path)

        # Process each video
        create_output_directories(["temp_frames"])

        for video_path in tqdm(video_files):
            person = detect_person_in_video(video_path, people_encodings)
            if person:
                os.makedirs(os.path.join(output_folder, person), exist_ok=True)
                output_path = os.path.join(output_folder, person, os.path.basename(video_path))
                shutil.move(video_path, output_path)

        if os.path.exists("temp_frames"):
            shutil.rmtree("temp_frames")