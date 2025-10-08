from markdown_to_blocks import markdown_to_blocks
from block_to_block_type import block_to_block_type, BlockType
from htmlnode import LeafNode, ParentNode
from text_to_textnodes import text_to_textnodes
from text_to_html import text_node_to_html_node
from bs4 import BeautifulSoup
from textnode import TextNode, TextType


def markdown_to_html_node(markdown):
    
    blocks = markdown_to_blocks(markdown)

    html_nodes = []
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

                # Split into lines and strip markdown
                lines = block.splitlines(keepends=True)
                parsed_lines = []

                # Remove the '>' and exactly one space if present
                for line in lines:
                    parsed_lines.append(line[1:].removeprefix(' '))

                # Split on double new lines, process inline markdown and create paragaph html tags
                paragraphs = "".join(parsed_lines).split('\n\n')

                quote_children = []

                for text in paragraphs:
                    children = text_to_children(text)
                    quote_children.append(ParentNode('p', children))

                html_nodes.append(ParentNode('blockquote', quote_children))

            # case BlockType.UNORDERED_LIST:

            # case BlockType.ORDERED_LIST:

            
    
    return ParentNode('div', html_nodes)

        
def text_to_children(text):

    text_nodes = text_to_textnodes(text)

    children = []

    for node in text_nodes:
        children.append(text_node_to_html_node(node))  

    return children

def get_header_tag(text):
    return f'h{text.find(' ')}'



md = """
# This is a header

This is **bolded** paragraph
text in a p
tag here

```
for line in lines:
    print(line)
return None
```



This is another paragraph with _italic_ text and `code` here

>     quoteblock
>type thing
>
> here
> with odd spacing

"""

output = """<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>"""
node = markdown_to_html_node(md)
html = node.to_html()

soup = BeautifulSoup(html, 'html.parser')
pretty_html = soup.prettify()
print(pretty_html)
print(pretty_html == output)
