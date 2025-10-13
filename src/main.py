from utils import copy_dir, clean_dir

def main():

   clean_dir('public')
   copy_dir('static', 'public')
    
if __name__ == "__main__":
    main()