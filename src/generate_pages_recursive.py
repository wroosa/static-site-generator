from generate_page import generate_page
from utils import path_in_working_dir
from pathlib import Path

def generate_pages_rescursive(dir_path_contet, template_path, dest_dir_path):

    # Check paths are in working directory and are directories
    working_path = Path().resolve()
    dest_path = (working_path / Path(dest_dir_path)).resolve()
    cont_path = (working_path / Path(dir_path_contet)).resolve()
    temp_path = (working_path / Path(template_path)).resolve()

    if not path_in_working_dir(dest_path):
        raise Exception("Error: page destination path is not in the working directory")
    
    if not path_in_working_dir(cont_path):
        raise Exception("Error: page content path is not in the working directory")
    
    if not path_in_working_dir(temp_path):
        raise Exception("Error: page template path is not in the working directory")
                        
    if not dest_path.is_dir():
        raise Exception("Error: page destination path is not a directory")
    
    if not cont_path.is_dir():
        raise Exception("Error: page content path is not a directory")
    
    if not temp_path.is_file():
        raise Exception("Error: page template path is not a file")
    
    # Recursive helper function to run after validating arguments
    def _gen_pages_recursive(c_path, t_path, d_path):

        items = c_path.iterdir()

        for item in items:
            dest_path = (d_path / item.name)
            if item.is_dir():
                dest_path.mkdir()
                _gen_pages_recursive(item, t_path, dest_path)
            elif item.suffix == '.md':
                generate_page(item, t_path, dest_path.with_suffix('.html'))
    
    return _gen_pages_recursive(cont_path, temp_path, dest_path)
    

    
    
    
