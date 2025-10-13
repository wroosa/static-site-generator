from pathlib import Path
import shutil

def copy_dir(from_dir, to_dir):
    
    # Safety check to make sure the paths are in the working directory and are not files
    working_path = Path().resolve()
    to_path = (working_path / Path(to_dir)).resolve()
    from_path = (working_path / Path(from_dir)).resolve()

    if not path_in_working_dir(to_path):
        raise Exception('Error: Target path is outside of the project directory')
    
    if not path_in_working_dir(from_path):
        raise Exception('Error: From path is outside of the project directory')
    
    if to_path.is_file():
        raise Exception("Error: Target path is a file and not a directory")
    
    if from_path.is_file():
        raise Exception("Error: From path is a file and not a directory")

    # Easy method
    # from_path.copy_into(to_path)

    # Recursive Method
    copy_dir_rec(from_path, to_path)

    return None


def copy_dir_rec(from_path, to_path):
    
    items = from_path.iterdir()

    for item in items:
        if item.is_dir():
            to = (to_path / item.name)
            to.mkdir()
            copy_dir_rec(item, to)
        else:
            item.copy(to_path / item.name)

def path_in_working_dir(path):

    working_path = Path().resolve()
    
    if working_path not in path.parents and working_path != path:
        return False
    else:
        return True
    
def clean_dir(path):

    working_path = Path().resolve()
    path_to_clean = (working_path / Path(path)).resolve()

    # Make sure the path is not a file and is in the working directory
    if not path_in_working_dir(path_to_clean):
        raise Exception("Error: Path to clean is outside the working directory")
    if path_to_clean.is_file():
        raise Exception("Error: Path to clean is a file and not a directory")
    
    # Delete all items in the target directory
    try:
        for item in path_to_clean.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    except:
        raise Exception(f'Error deleting contents of public directory')