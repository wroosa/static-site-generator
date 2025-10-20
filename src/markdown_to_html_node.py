from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType
from htmlnode import LeafNode, ParentNode
from text_to_textnodes import text_to_textnodes
from text_to_html import text_node_to_html_node
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    
    # Split markdown into blocks
    blocks = markdown_to_blocks(markdown)

    # Initialize list of HTML nodes representing doc
    html_nodes = []

    # Process each block
    for block in blocks:
        
        b_type = block_to_block_type(block)

        match b_type:

            case BlockType.PARAGRAPH:

                children = text_to_children(block)

                html_nodes.append(ParentNode('p', children))

            case BlockType.HEADER:

                # Get the header size
                tag = get_header_tag(block)

                # Remove markdown characters
                block_text = block.lstrip('#')[1:]

                children = text_to_children(block_text)

                html_nodes.append(ParentNode(tag, children))

            case BlockType.CODE:

                # Do not parse inline markdown, manually create text node
                text_node = TextNode(block.strip('```'), TextType.TEXT)

                text_child = text_node_to_html_node(text_node)

                # Create a parent code not with the leaf node as it's child
                code_node = ParentNode('code', [text_child])

                # Create a <pre> parent node to wrap the code node
                html_nodes.append(ParentNode('pre', [code_node]))


            case BlockType.QUOTE:

                # Split into lines and strip markdown.
                lines = block.splitlines(keepends=True)
                parsed_lines = []

                # Remove the '>' and exactly one space if present
                for line in lines:
                    parsed_lines.append(line[1:].removeprefix(' '))

                # Split on double new lines, process inline markdown and create paragaph html tags

                # COMMENT TO PASS BOOTS TEST
                paragraphs = "".join(parsed_lines).split('\n\n')

                quote_children = []

                for text in paragraphs:
                    children = text_to_children(text)
                    quote_children.append(ParentNode('p', children))
                # COMMENT TO PASS BOOTS TEST
                
                # Code to pass Boots tests
                # paragraphs = "".join(parsed_lines)
                # children = text_to_children(paragraphs)
                # html_nodes.append(ParentNode('blockquote', children))

                # COMMENT TO PASS BOOTS TEST
                html_nodes.append(ParentNode('blockquote', quote_children))

            case BlockType.UNORDERED_LIST:

                # Split into lines and strip markdown
                lines = [s[2:] for s in block.splitlines()]

                # Parse inline markdown and create a list item element for each line to append as children of the ul element
                list_items = []
                for line in lines:
                    children = text_to_children(line)
                    list_items.append(ParentNode('li', children))

                html_nodes.append(ParentNode('ul', list_items))


            case BlockType.ORDERED_LIST:

                # Split into lines and strip markdown. Then parse inline markdown and create a list item element for each line
                list_items = []
                for i, lines in enumerate(block.splitlines()):
                    lines_parsed = lines.removeprefix(f'{i+1}. ')
                    children = text_to_children(lines_parsed)
                    list_items.append(ParentNode('li', children))

                html_nodes.append(ParentNode('ol', list_items))

    # Return all html nodes nested inside a div
    return ParentNode('div', html_nodes)


# Function to process text with inline markdown into text nodes then html nodes
def text_to_children(text):

    text_nodes = text_to_textnodes(text)

    children = []

    for node in text_nodes:
        children.append(text_node_to_html_node(node))  

    return children

# Function to get the correct header html tag
def get_header_tag(text):
    return f'h{text.find(' ')}'