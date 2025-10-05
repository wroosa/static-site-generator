from pprint import pprint
from split_nodes_delimiter import split_nodes_delimiter
from split_nodes_img_and_links import split_nodes_images, split_nodes_links
from textnode import TextType, TextNode


def text_to_textnodes(text):

    # Empty strings should return no nodes
    if text == "":
        return []
    
    # Create a text node from intial text
    text_nodes = [TextNode(text, TextType.TEXT)]

    # Text types to call delimiter splits on
    emphasis_types = [
        TextType.BOLD,
        TextType.ITALIC,
        TextType.CODE,
    ]

    # Call delimiter split for all text emphasis types
    for text_type in emphasis_types:
        text_nodes = split_nodes_delimiter(text_nodes, text_type.value, text_type)

    # Split out images and links
    text_nodes = split_nodes_images(text_nodes)
    text_nodes = split_nodes_links(text_nodes)

    return text_nodes
