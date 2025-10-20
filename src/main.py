from utils import copy_dir, clean_dir
from generate_pages_recursive import generate_pages_rescursive
import argparse

def main():

   parser = argparse.ArgumentParser(
      prog="Static Site Generator",
      description="Generates a static site from markdown files")
   
   parser.add_argument(
      '-basepath',
      type=str,
      default='/',
      help='Path to the working directory')
   
   base_path = parser.parse_args().basepath

   clean_dir('docs')
   copy_dir('static', 'docs')
   generate_pages_rescursive('content', 'templates/template.html', 'docs', base_path)
    
if __name__ == "__main__":
    main()