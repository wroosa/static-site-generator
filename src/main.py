from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    test_node = TextNode(
        "A freakin' cool link",
        TextType.LINK,
        'https://isitchristmas.com/',
    )
    childNode1 = HTMLNode("p", "This is a child", props={'class': 'child'})
    childNode2 = HTMLNode("a", "This is a child")
    node = HTMLNode(
        "div", 
        "This is a div boi!", 
        [childNode1, childNode2], 
        {'class': 'nav-list', 'href': 'link.com'},
    )

    print(node.props_to_html())

if __name__ == "__main__":
    main()