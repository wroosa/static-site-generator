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

        node_list = [TextNode("Many `spl`it` `parts`!`", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_result = [
            TextNode("Many ", TextType.TEXT),
            TextNode("spl", TextType.CODE),
            TextNode("it", TextType.TEXT),
            TextNode(" ", TextType.CODE),
            TextNode("parts", TextType.TEXT),
            TextNode("!", TextType.CODE)
        ]
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

        node_list = [TextNode("Many **spl**it** **parts**!**", TextType.TEXT)]
        result = split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_result = [
            TextNode("Many ", TextType.TEXT),
            TextNode("spl", TextType.BOLD),
            TextNode("it", TextType.TEXT),
            TextNode(" ", TextType.BOLD),
            TextNode("parts", TextType.TEXT),
            TextNode("!", TextType.BOLD)
        ]

    def test_split_single_node_invalid(self):
        
        node_list = [TextNode("Text with bad **bold in it", TextType.TEXT)]
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter(node_list, "**", TextType.BOLD)
        expected_message = "Unmatched delimiter: invalid markdown"
        self.assertEqual(str(cm.exception), expected_message)


        node_list = [TextNode("`Text with bad code starting", TextType.TEXT)]
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_message = "Unmatched delimiter: invalid markdown"
        self.assertEqual(str(cm.exception), expected_message)

        node_list = [TextNode("Text with bad italic ending_", TextType.TEXT)]
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter(node_list, "_", TextType.ITALIC)
        expected_message = "Unmatched delimiter: invalid markdown"
        self.assertEqual(str(cm.exception), expected_message)

        node_list = [TextNode("Ran`dom` del`ims `and` lengths", TextType.TEXT)]
        with self.assertRaises(Exception) as cm:
            split_nodes_delimiter(node_list, "`", TextType.CODE)
        expected_message = "Unmatched delimiter: invalid markdown"
        self.assertEqual(str(cm.exception), expected_message)