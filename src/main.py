from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

def main():
    test_node = TextNode(
        "A freakin' cool link",
        TextType.LINK,
        'https://isitchristmas.com/',
    )
    node = LeafNode(
            "div", 
            "This is a div boi!",
            {'class': 'nav-list', 'href': 'link.com'},
        )

    print(node.to_html())

if __name__ == "__main__":
    main()