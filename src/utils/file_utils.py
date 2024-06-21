import json
import os
import pickle
from typing import Union

import PIL


def save_text_to_file(text: str, output_path: str):
    """
    Saves text to a file.

    Args:
        text (str): The extracted text from the document.
        output_path (str): The path of the processed document

    Returns:
        str: The path to the saved text file.
    """
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(text)


def read_text_from_file(file_path: str) -> str:
    """
    Reads and returns the entire content of a text file.

    Args:
        file_path (str): The path to the file that needs to be read.

    Returns:
        str: The content of the file as a string.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def save_as_pickle(obj: any, file_path: str):
    """
    Saves an object to a pickle file.

    Parameters:
        obj (any): The Python object to be serialized and saved.
        file_path (str): The path to the file where the object should be saved.
    """
    with open(file_path, "wb") as file:
        pickle.dump(obj, file)


def load_from_pickle(file_path: str) -> any:
    """
    Loads an object from a pickle file.

    Parameters:
        file_path (str): The path to the pickle file from which to load the object.

    Returns:
        any: The Python object that was deserialized from the pickle file.
    """
    with open(file_path, "rb") as file:
        return pickle.load(file)


def save_as_json(obj: Union[dict, list], file_path: str) -> None:
    """
    Save a Python dictionary or list to a file in JSON format.

    Parameters:
    - obj (dict or list): The dictionary or list to be saved as a JSON file.
    - file_path (str): The path of the file where the JSON data will be saved.

    Returns:
    - None
    """
    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(obj, json_file, ensure_ascii=False, indent=4)


def load_json(file_path: str) -> dict:
    """
    TODO
    """
    with open(file_path, 'r', encoding="utf-8") as f:
        return json.load(f)


def create_directories_for_file(file_path):
    """
    Creates all necessary parent directories for the given file path if they do not already exist.

    This function takes a file path, extracts its directory path, and ensures that this directory
    path exists by creating any missing directories in the path. It uses the `os.makedirs()` function
    with `exist_ok=True` to prevent raising an error if the directory already exists.

    Args:
        file_path (str): The full path to a file for which directories need to be created.
    """
    directory_path = os.path.dirname(file_path)
    os.makedirs(directory_path, exist_ok=True)


def save_png_image(image: PIL.Image, output_path: str):
    """
    Saves a PNG image to a file.

    Args:
        image (PIL.Image.Image): The image to be saved to a file.
        output_path (str): The path of the image

    Returns:
        str: The path to the saved text file.
    """
    image.save(output_path, "PNG")
