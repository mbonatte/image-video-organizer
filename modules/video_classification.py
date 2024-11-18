import cv2
import os
from pathlib import Path

def extract_frames_from_video(video_path, frame_interval=30):
    """
    Extract frames from the video at regular intervals.
    Args:
        video_path (str): Path to the video file.
        frame_interval (int): Number of frames to skip before saving the next frame.
    Returns:
        list: List of extracted frame file paths.
    """
    video_capture = cv2.VideoCapture(video_path)
    frame_count = 0
    extracted_frames = []

    while video_capture.isOpened():
        success, frame = video_capture.read()
        if not success:
            break
        if frame_count % frame_interval == 0:
            frame_filename = f"{Path(video_path).stem}_frame_{frame_count}.jpg"
            frame_filepath = os.path.join("temp_frames", frame_filename)
            cv2.imwrite(frame_filepath, frame)
            extracted_frames.append(frame_filepath)
        frame_count += 1

    video_capture.release()
    return extracted_frames



    