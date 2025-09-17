from textnode import TextNode, TextType

def main():
    test_node = TextNode(
        "A freakin' cool link",
        TextType.LINK,
        'https://isitchristmas.com/',
    )
    print(test_node)

if __name__ == "__main__":
    main()