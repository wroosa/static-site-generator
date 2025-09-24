import unittest

from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from text_to_html import text_node_to_html_node

class TestTextToHTML(unittest.TestCase):

    def test_text(self):
        node = TextNode("This is a text node", TextType.PLAIN)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("bold type stuff", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'b')
        self.assertEqual(html_node.value, "bold type stuff")

    def test_italic(self):
        node = TextNode("pizza Pizza", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'i')
        self.assertEqual(html_node.value, "pizza Pizza")
    
    def test_code(self):
        node = TextNode("Hax0r L33t", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'code')
        self.assertEqual(html_node.value, "Hax0r L33t")

    def test_link(self):
        node = TextNode("url type stuff", TextType.LINK, 'www.google.com')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'a')
        self.assertEqual(html_node.value, "url type stuff")
        self.assertEqual(html_node.props, { 'href': 'www.google.com'})

    def test_image(self):
        node = TextNode("picture of banana", TextType.IMAGE, 'https://upload.wikimedia.org/wikipedia/commons/d/de/Bananavarieties.jpg')
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, 'img')
        self.assertEqual(html_node.value, '')
        self.assertEqual(html_node.props, { 'src': 'https://upload.wikimedia.org/wikipedia/commons/d/de/Bananavarieties.jpg', 'alt': 'picture of banana'})