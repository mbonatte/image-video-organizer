import face_recognition
import os

def load_encodings_for_each_person(subfolders):
    people_encodings = {}
    for subfolder in subfolders:
        person_name = os.path.basename(subfolder).split(' ', 1)[-1]  # Extract the name after the number
        encodings = load_reference_encodings(subfolder)
        if encodings:
            people_encodings[person_name] = encodings
    return people_encodings

def load_reference_encodings(reference_folder):
    """Load face encodings from reference photos."""
    encodings = []
    for file in os.listdir(reference_folder):
        file_path = os.path.join(reference_folder, file)
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            try:
                image = face_recognition.load_image_file(file_path)
                encoding = face_recognition.face_encodings(image)
                if encoding:
                    encodings.append(encoding[0])
            except Exception as e:
                print(f"Error processing reference image {file_path}: {e}")
    return encodings

def contains_face(image_path, reference_encodings, tolerance=0.5):
    """Check if the image contains any of the known faces."""
    try:
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        if not face_locations:
            return False
        if reference_encodings is None:
            return True
        face_encodings = face_recognition.face_encodings(image, face_locations)
        for encoding in face_encodings:
            matches = face_recognition.compare_faces(reference_encodings, encoding, tolerance=tolerance)
            if any(matches):
                return True
        
    except Exception as e:
        print(f"Error processing {image_path}: {e}")
    return False
