import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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
        
class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_many_grandchildren(self):
            grandchild_node1 = LeafNode("b", "grandchild")
            grandchild_node2 = LeafNode("b", "grandchild", { 'class': 'baby'})
            child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
            parent_node = ParentNode("div", [child_node])
            self.assertEqual(
                parent_node.to_html(),
                "<div><span><b>grandchild</b><b class=baby>grandchild</b></span></div>",
            )

if __name__ == "__main__":
    unittest.main()