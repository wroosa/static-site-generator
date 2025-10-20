import unittest

from text_to_textnodes import text_to_textnodes
from textnode import TextNode, TextType


class TestTextToTextNodes(unittest.TestCase):
    def test_plain_text_returns_single_text_node(self):
        s = "Hello world."
        out = text_to_textnodes(s)
        self.assertEqual(out, [TextNode("Hello world.", TextType.TEXT)])

    def test_bold_only(self):
        s = "This is **bold** text."
        out = text_to_textnodes(s)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text.", TextType.TEXT),
        ]
        self.assertEqual(out, expected)

    def test_italic_only(self):
        # Works whether your italic delimiter is '*' or '_' — relies on your split function
        s = "A _simple_ case."
        out = text_to_textnodes(s)
        expected = [
            TextNode("A ", TextType.TEXT),
            TextNode("simple", TextType.ITALIC),
            TextNode(" case.", TextType.TEXT),
        ]
        self.assertEqual(out, expected)

    def test_code_only(self):
        s = "run `make build` now"
        out = text_to_textnodes(s)
        expected = [
            TextNode("run ", TextType.TEXT),
            TextNode("make build", TextType.CODE),
            TextNode(" now", TextType.TEXT),
        ]
        self.assertEqual(out, expected)

    def test_mixed_emphasis_in_one_string(self):
        s = "This has **bold**, _italic_, and `code`."
        out = text_to_textnodes(s)
        expected = [
            TextNode("This has ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(", ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(", and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(out, expected)

    def test_multiple_segments_of_same_emphasis(self):
        s = "**one** and **two**"
        out = text_to_textnodes(s)
        expected = [
            TextNode("one", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("two", TextType.BOLD),
        ]
        self.assertEqual(out, expected)

    def test_link_extraction(self):
        s = "Read the [docs](https://example.com/docs)."
        out = text_to_textnodes(s)
        expected = [
            TextNode("Read the ", TextType.TEXT),
            TextNode("docs", TextType.LINK, "https://example.com/docs"),
            TextNode(".", TextType.TEXT),
        ]
        self.assertEqual(out, expected)

    def test_image_extraction(self):
        s = "Here is a logo ![Logo](https://img.example.com/logo.png)"
        out = text_to_textnodes(s)
        expected = [
            TextNode("Here is a logo ", TextType.TEXT),
            TextNode("Logo", TextType.IMAGE, "https://img.example.com/logo.png"),
        ]
        self.assertEqual(out, expected)

    def test_nodes_with_both_images_and_links(self):
        s = "See ![Alt](https://x/y.png) and visit [site](https://example.com)"
        out = text_to_textnodes(s)
        expected = [
            TextNode("See ", TextType.TEXT),
            TextNode("Alt", TextType.IMAGE, "https://x/y.png"),
            TextNode(" and visit ", TextType.TEXT),
            TextNode("site", TextType.LINK, "https://example.com"),
        ]
        self.assertEqual(out, expected)

    def test_emphasis_adjacent_to_link_and_image(self):
        s = "**Bold** then [link](https://a) then `code` then ![img](https://b)"
        out = text_to_textnodes(s)
        expected = [
            TextNode("Bold", TextType.BOLD),
            TextNode(" then ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://a"),
            TextNode(" then ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" then ", TextType.TEXT),
            TextNode("img", TextType.IMAGE, "https://b"),
        ]
        self.assertEqual(out, expected)

    def test_malformed_unmatched_bold_delimiter_left_as_text(self):
        s = "This **is not closed"
        with self.assertRaises(Exception) as cm:
            text_to_textnodes(s)
        expected_message = "Unmatched delimiter: invalid markdown"
        self.assertEqual(str(cm.exception), expected_message)

    def test_malformed_link_left_as_text(self):
        s = "Broken [link](missing-closing"
        out = text_to_textnodes(s)
        self.assertEqual(out, [TextNode("Broken [link](missing-closing", TextType.TEXT)])

    def test_malformed_image_left_as_text(self):
        s = "Broken ![alt](no-end"
        out = text_to_textnodes(s)
        self.assertEqual(out, [TextNode("Broken ![alt](no-end", TextType.TEXT)])

    def test_empty_string(self):
        out = text_to_textnodes("")
        self.assertEqual(out, [])

    def test_only_image(self):
        s = "![x](u)"
        out = text_to_textnodes(s)
        self.assertEqual(out, [TextNode("x", TextType.IMAGE, "u")])

    def test_only_link(self):
        s = "[x](u)"
        out = text_to_textnodes(s)
        self.assertEqual(out, [TextNode("x", TextType.LINK, "u")])

    def test_back_to_back_emphasis(self):
        s = "**a****b**"
        out = text_to_textnodes(s)
        expected = [
            TextNode("a", TextType.BOLD),
            TextNode("b", TextType.BOLD),
        ]
        self.assertEqual(out, expected)


if __name__ == "__main__":
    unittest.main()