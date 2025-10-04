# test_split_nodes_img_and_links.py
import unittest
from split_nodes_img_and_links import split_nodes_images, split_nodes_links
from textnode import TextNode, TextType


class TestSplitNodesImages(unittest.TestCase):
    def test_passthrough_non_text_nodes(self):
        old = [
            TextNode("already image", TextType.IMAGE, "http://img"),
            TextNode("already link", TextType.LINK, "http://x"),
        ]
        self.assertEqual(split_nodes_images(old), old)

    def test_no_images_found_keeps_text(self):
        old = [TextNode("no images here", TextType.TEXT)]
        self.assertEqual(split_nodes_images(old), old)

    def test_single_image_in_middle(self):
        old = [TextNode("alpha ![alt](http://u) omega", TextType.TEXT)]
        expected = [
            TextNode("alpha ", TextType.TEXT),
            TextNode("alt", TextType.IMAGE, "http://u"),
            TextNode(" omega", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images(old), expected)

    def test_two_images_adjacent(self):
        old = [TextNode("X![a](u)![b](v)Y", TextType.TEXT)]
        expected = [
            TextNode("X", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "u"),
            TextNode("", TextType.TEXT),  # empty between adjacent images
            TextNode("b", TextType.IMAGE, "v"),
            TextNode("Y", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images(old), expected)

    def test_image_at_start_and_trailing_text(self):
        old = [TextNode("![a](u) tail", TextType.TEXT)]
        expected = [
            TextNode("", TextType.TEXT),  # empty before start image
            TextNode("a", TextType.IMAGE, "u"),
            TextNode(" tail", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images(old), expected)

    def test_image_at_end(self):
        old = [TextNode("head ![a](u)", TextType.TEXT)]
        expected = [
            TextNode("head ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "u"),
        ]
        self.assertEqual(split_nodes_images(old), expected)

    def test_mixed_input_non_text_and_text(self):
        old = [
            TextNode("keep me", TextType.BOLD),
            TextNode("x ![a](u) y", TextType.TEXT),
        ]
        expected = [
            TextNode("keep me", TextType.BOLD),
            TextNode("x ", TextType.TEXT),
            TextNode("a", TextType.IMAGE, "u"),
            TextNode(" y", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images(old), expected)

    # --- Malformed image markdown should NOT split ---
    def test_malformed_image_missing_closing_paren(self):
        s = TextNode("text ![alt](http://u more", TextType.TEXT)
        self.assertEqual(split_nodes_images([s]), [s])

    def test_malformed_image_missing_alt_bracket(self):
        s = TextNode("text !alt](http://u)", TextType.TEXT)
        self.assertEqual(split_nodes_images([s]), [s])

    def test_malformed_image_spaces_break_syntax(self):
        s = TextNode("text ![alt] (http://u)", TextType.TEXT)  # space before '('
        self.assertEqual(split_nodes_images([s]), [s])

    # --- Nodes containing both images and links (images should split; links remain as text) ---
    def test_images_and_links_image_then_link(self):
        s = TextNode("a ![i](u) and [t](v) z", TextType.TEXT)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("i", TextType.IMAGE, "u"),
            TextNode(" and [t](v) z", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images([s]), expected)

    def test_images_and_links_link_then_image(self):
        s = TextNode("a [t](v) and ![i](u) z", TextType.TEXT)
        expected = [
            TextNode("a [t](v) and ", TextType.TEXT),
            TextNode("i", TextType.IMAGE, "u"),
            TextNode(" z", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images([s]), expected)

    def test_images_and_links_adjacent(self):
        s = TextNode("![i](u)[t](v)", TextType.TEXT)
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("i", TextType.IMAGE, "u"),
            TextNode("[t](v)", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_images([s]), expected)


class TestSplitNodesLinks(unittest.TestCase):
    def test_passthrough_non_text_nodes(self):
        old = [
            TextNode("already image", TextType.IMAGE, "http://img"),
            TextNode("already bold", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_links(old), old)

    def test_no_links_found_keeps_text(self):
        old = [TextNode("no links here", TextType.TEXT)]
        self.assertEqual(split_nodes_links(old), old)

    def test_single_link_in_middle(self):
        old = [TextNode("pre [txt](http://x) post", TextType.TEXT)]
        expected = [
            TextNode("pre ", TextType.TEXT),
            TextNode("txt", TextType.LINK, "http://x"),
            TextNode(" post", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_links(old), expected)

    def test_two_links_adjacent(self):
        old = [TextNode("X[a](u)[b](v)Y", TextType.TEXT)]
        expected = [
            TextNode("X", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
            TextNode("", TextType.TEXT),
            TextNode("b", TextType.LINK, "v"),
            TextNode("Y", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_links(old), expected)

    def test_link_at_start_and_trailing_text(self):
        old = [TextNode("[a](u) tail", TextType.TEXT)]
        expected = [
            TextNode("", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
            TextNode(" tail", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_links(old), expected)

    def test_link_at_end(self):
        old = [TextNode("head [a](u)", TextType.TEXT)]
        expected = [
            TextNode("head ", TextType.TEXT),
            TextNode("a", TextType.LINK, "u"),
        ]
        self.assertEqual(split_nodes_links(old), expected)

    # --- Malformed link markdown should NOT split ---
    def test_malformed_link_missing_closing_paren(self):
        s = TextNode("text [txt](http://x more", TextType.TEXT)
        self.assertEqual(split_nodes_links([s]), [s])

    def test_malformed_link_missing_text_bracket(self):
        s = TextNode("text txt](http://x)", TextType.TEXT)
        self.assertEqual(split_nodes_links([s]), [s])

    def test_malformed_link_spaces_break_syntax(self):
        s = TextNode("text [txt] (http://x)", TextType.TEXT)  # space before '('
        self.assertEqual(split_nodes_links([s]), [s])

    # --- Nodes containing both images and links (links should split; images remain as text) ---
    def test_links_and_images_link_then_image(self):
        s = TextNode("a [t](v) and ![i](u) z", TextType.TEXT)
        expected = [
            TextNode("a ", TextType.TEXT),
            TextNode("t", TextType.LINK, "v"),
            TextNode(" and ![i](u) z", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_links([s]), expected)

    def test_links_and_images_image_then_link(self):
        s = TextNode("a ![i](u) and [t](v) z", TextType.TEXT)
        expected = [
            TextNode("a ![i](u) and ", TextType.TEXT),
            TextNode("t", TextType.LINK, "v"),
            TextNode(" z", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_links([s]), expected)

    def test_links_and_images_adjacent(self):
        s = TextNode("![i](u)[t](v)", TextType.TEXT)
        expected = [
            TextNode("![i](u)", TextType.TEXT),
            TextNode("t", TextType.LINK, "v"),
        ]
        self.assertEqual(split_nodes_links([s]), expected)


if __name__ == "__main__":
    unittest.main()

