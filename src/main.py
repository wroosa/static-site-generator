from utils import copy_dir, clean_dir
from generate_pages_recursive import generate_pages_rescursive

def main():

   clean_dir('public')
   copy_dir('static', 'public')
   generate_pages_rescursive('content', 'template.html', 'public')
    
if __name__ == "__main__":
    main()