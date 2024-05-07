import pickle


def save_to_pickle(obj: any, file_path: str):
    """
    Saves an object to a pickle file.

    Parameters:
        obj (any): The Python object to be serialized and saved.
        file_path (str): The path to the file where the object should be saved.
    """
    with open(file_path, 'wb') as file:
        pickle.dump(obj, file)

def load_from_pickle(file_path: str) -> any:
    """
    Loads an object from a pickle file.

    Parameters:
        file_path (str): The path to the pickle file from which to load the object.

    Returns:
        any: The Python object that was deserialized from the pickle file.
    """
    with open(file_path, 'rb') as file:
        return pickle.load(file)

        