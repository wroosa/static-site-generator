import unittest

from textnode import TextNode, TextType

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node, node2)
        node = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        node2 = TextNode("This is a text node", TextType.IMAGE, "www.google.com")
        self.assertEqual(node, node2)


    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC, "www.google.com")
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)
        node = TextNode("This is a text node", TextType.PLAIN)
        node2 = TextNode("This is a image node", TextType.PLAIN)
        self.assertNotEqual(node, node2)
        node = TextNode("This is a text node", TextType.LINK, "url")
        node2 = TextNode("This is a text node", TextType.LINK, "different.url")
        self.assertNotEqual(node, node2)

if __name__ == "__main__":
    unittest.main()