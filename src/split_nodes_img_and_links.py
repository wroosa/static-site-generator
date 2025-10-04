from textnode import TextNode, TextType
from extract_img_and_links import extract_markdown_links, extract_markdown_images


def split_nodes_images(old_nodes):
    
    # new list of nodes
    new_nodes = []

    for node in old_nodes:
        
        # Only split nodes that are text
        if node.text_type != TextType.TEXT:

            # Append non-text nodes as is
            new_nodes.append(node)

        else:

            # Get all images in the text
            images = extract_markdown_images(node.text)

            # If no images are found simply append the node as is
            if images == []:
                new_nodes.append(node)
            else:

                remaining_text = node.text

                # Extract each image
                for image in images:
                    markdown = f'![{image[0]}]({image[1]})'

                    parts = remaining_text.split(markdown, 1)

                    pre_text_node = TextNode(parts[0], TextType.TEXT)
                    new_nodes.append(pre_text_node)

                    image_node = TextNode(image[0], TextType.IMAGE, image[1])
                    new_nodes.append(image_node)

                    remaining_text = parts[1]

                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                
    return new_nodes

def split_nodes_links(old_nodes):
    
    # new list of nodes
    new_nodes = []

    for node in old_nodes:
        
        # Only split nodes that are text
        if node.text_type != TextType.TEXT:

            # Append non-text nodes as is
            new_nodes.append(node)

        else:

            # Get all links in the text
            links = extract_markdown_links(node.text)

            # If no links are found simply append the node as is
            if links == []:
                new_nodes.append(node)

            else:

                remaining_text = node.text

                # Extract each link
                for link in links:
                    markdown = f'[{link[0]}]({link[1]})'

                    parts = remaining_text.split(markdown, 1)

                    pre_text_node = TextNode(parts[0], TextType.TEXT)
                    new_nodes.append(pre_text_node)

                    link_node = TextNode(link[0], TextType.LINK, link[1])
                    new_nodes.append(link_node)

                    remaining_text = parts[1]

                if remaining_text != "":
                    new_nodes.append(TextNode(remaining_text, TextType.TEXT))
                
    return new_nodes
