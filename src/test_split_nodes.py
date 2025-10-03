import unittest

from textnode import TextType, TextNode
from split_nodes_delimiter import split_nodes_delimiter

class TestSplitNodes(unittest.TestCase):

    def test_split_single_nodes_code(self):
        
        node_list = [TextNode("Just a text node", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(node_list, "`", TextType.CODE),
            [TextNode("Just a text node", TextType.TEXT)]
        )

        node_list = [TextNode("Text with some `code` in it", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_result = [
            TextNode("Text with some ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" in it", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

        node_list = [TextNode("`Starts` and ends with `code`", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_result = [
            TextNode("Starts", TextType.CODE),
            TextNode(" and ends with ", TextType.TEXT),
            TextNode("code", TextType.CODE)
        ]
        self.assertEqual(result, expected_result)

        node_list = [TextNode("delim ``in be`tween`` delim", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_result = [
            TextNode("delim ", TextType.TEXT),
            TextNode("in be`tween", TextType.CODE),
            TextNode(" delim", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

        node_list = [TextNode("start ``with no `end", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_result = [TextNode("start ``with no `end", TextType.TEXT)]
        self.assertEqual(result, expected_result)

    def test_split_single_nodes_others(self):
        
        node_list = [TextNode("Just a text node", TextType.TEXT)]
        self.assertEqual(
            split_nodes_delimiter(node_list, "**", TextType.BOLD),
            [TextNode("Just a text node", TextType.TEXT)]
        )

        node_list = [TextNode("Text with some **bold** in it", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_result = [
            TextNode("Text with some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" in it", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)

        node_list = [TextNode("_Starts_ and ends with _italic_", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "_", TextType.ITALIC)
        expected_result = [
            TextNode("Starts", TextType.ITALIC),
            TextNode(" and ends with ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC)
        ]
        self.assertEqual(result, expected_result)

        node_list = [TextNode("**Start** and end **BOLD**", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_result = [
            TextNode("Start", TextType.BOLD),
            TextNode(" and end ", TextType.TEXT),
            TextNode("BOLD", TextType.BOLD)
        ]
        self.assertEqual(result, expected_result)

        node_list = [TextNode("delim ****be**tween**** delim", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_result = [
            TextNode("delim ", TextType.TEXT),
            TextNode("be**tween", TextType.CODE),
            TextNode(" delim", TextType.TEXT)
        ]
        self.assertEqual(result, expected_result)
            