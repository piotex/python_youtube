import os


def create_directory_if_missing(directory_path: str):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


# Usage example:
