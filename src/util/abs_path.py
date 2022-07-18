import os
def path(__file, file) -> str:
    dir_path = os.path.dirname(os.path.realpath(__file))
    return os.path.join(dir_path, file)