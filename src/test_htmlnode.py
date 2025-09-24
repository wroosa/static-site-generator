import unittest

from htmlnode import HTMLNode

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

    def test_repr(self):
        self.assertEqual(
            self.node.__repr__(),
            (
                "HTMLNode(tag=div, value=This is a div boi!, children=None, " "props={'class': 'nav-list', 'href': 'link.com'})"
            )
        )
        


if __name__ == "__main__":
    unittest.main()