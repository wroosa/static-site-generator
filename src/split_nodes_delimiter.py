from textnode import TextType, TextNode

# Helper function to skip elements of an enum
def skip(iterator, n):
    for _ in range(n):
        next(iterator, None)

def split_nodes_delimiter(old_nodes, delimiter, text_type):

    # new list of nodes
    new_nodes = []

    for node in old_nodes:

        # Only split nodes that are text
        if node.text_type != TextType.TEXT:

            # Append non-text nodes as is
            new_nodes.append(node)
        
        else:
            
            # Split the node on the delimiter
            parts = node.text.split(delimiter)

            # If there are unmatched delimiters throw an exception
            if len(parts) % 2 == 0:
                raise Exception("Unmatched delimiter: invalid markdown")
            
            for i, part in enumerate(parts):

                # Do not add empty strings to the new node list
                if part == "":
                    continue

                # Odd parts are text and even parts are the given text_type
                if i % 2 == 0:
                    new_nodes.append(TextNode(part, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(part, text_type))
        
    return new_nodes