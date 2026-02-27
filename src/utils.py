import os
import yaml


# ---------------------------------------
# YAML UTILITIES
# ---------------------------------------
def load_yaml(path: str) -> dict:
    """
    Load a YAML file and return dictionary.
    """
    with open(path, "r") as f:
        return yaml.safe_load(f)


def save_yaml(path: str, data: dict):
    """
    Save dictionary to YAML file.
    """
    with open(path, "w") as f:
        yaml.safe_dump(data, f)


# ---------------------------------------
# DIRECTORY UTILITIES
# ---------------------------------------
def create_directories(paths: list):
    """
    Create multiple directories if they don't exist.
    """
    for path in paths:
        os.makedirs(path, exist_ok=True)


# ---------------------------------------
# FILE UTILITIES
# ---------------------------------------
def file_exists(path: str) -> bool:
    """
    Check if file exists.
    """
    return os.path.exists(path)


def copy_file(source: str, destination: str):
    """
    Copy file from source to destination.
    """
    import shutil
    shutil.copy(source, destination)