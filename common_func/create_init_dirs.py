import os


def create_directory_if_missing(directory_path: str):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def create_file_if_missing(file_path: str):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            file.write("")

