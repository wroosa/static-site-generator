import unittest

from htmlnode import HTMLNode, LeafNode

class TestHTMLNode(unittest.TestCase):

    def setUp(self):
        self.node = HTMLNode(
            "div", 
            "This is a div boi!", 
            None, 
            {'class': 'nav-list', 'href': 'link.com'},
        )
    
    def test_props_to_html(self):
        self.assertEqual(self.node.props_to_html(), " class=nav-list href=link.com")
        self.assertNotEqual(self.node.props_to_html(), " class= href=")
        node = HTMLNode(
            "div", 
            "This is a div boi!", 
            None, 
            None,
        )
        self.assertEqual(node.props_to_html(), "")

    def test_repr(self):
        self.assertEqual(
            self.node.__repr__(),
            (
                "HTMLNode(tag=div, value=This is a div boi!, children=None, " "props={'class': 'nav-list', 'href': 'link.com'})"
            )
        )

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode(
            "div", 
            "This is a div boi!",
            {'class': 'nav-list', 'href': 'link.com'},
        )
        self.assertEqual(
            node.to_html(), 
            (
                "<div class=nav-list href=link.com>This is a div boi!</div>"
            )
        )
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        


if __name__ == "__main__":
    unittest.main()