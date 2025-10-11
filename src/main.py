from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode
from utils import copy_dir

def main():
   copy_dir('static', 'public')
    
if __name__ == "__main__":
    main()