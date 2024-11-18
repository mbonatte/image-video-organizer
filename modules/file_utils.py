import os

def create_output_directories(directories):
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def list_files_in_directory(source_folder, valid_extensions):
    valid_extensions_set = set(valid_extensions)
    return [
        os.path.join(root, file)
        for root, _, files in os.walk(source_folder)
        for file in files
        if os.path.splitext(file)[1].lower() in valid_extensions_set
    ]