import os


def path(__file: str, file: str) -> str:
    """
    Used to calculate the absolute path of a file based on the path to the calle. This is used to make the execution predictable regardless of where the program is run from and its current working directory.
    """
    dir_path = os.path.dirname(os.path.realpath(__file))
    return os.path.join(dir_path, file)