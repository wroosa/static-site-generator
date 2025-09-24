from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    test_node = TextNode(
        "A freakin' cool link",
        TextType.LINK,
        'https://isitchristmas.com/',
    )
    node = HTMLNode(
            "div", 
            "This is a div boi!", 
            None, 
            {'class': 'nav-list', 'href': 'link.com'},
        )
    
    node2 = HTMLNode(
            "div", 
            "This is a div boi!", 
            None, 
            {'class': 'nav-list', 'href': 'link.com'},
        )

    print(node.__repr__() == node2.__repr__())

if __name__ == "__main__":
    main()