# image-video-organizer
## Overview
image-video-organizer is a robust tool designed to classify and organize images and videos within a specific directory. It detects the folder to sort based on its structure and organizes files based on their content using face recognition, machine learning, and video frame analysis. Ideal for managing large multimedia collections with ease and efficiency.

## Usage
Ensure the following directory structure in the specific folder (media_root/):
- people_photos/: Contains subfolders for each person with their reference photos.
- A folder with media files to sort (detected automatically).
- folder_sorted/: The output directory for sorted files (if not present, it will be created).


## Output
The tool will:
Create or update the folder_sorted directory with subfolders:
- anonymous/: Images with unidentified faces.
- nature/: Nature-related images.
- others/: Files that do not match any specific category.
- Subfolders for each identified person based on reference photos.