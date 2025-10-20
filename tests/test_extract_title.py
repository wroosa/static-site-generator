import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):

    def test_single_valid_title(self):
        md = "# My Title"
        self.assertEqual(extract_title(md), "My Title")

    def test_title_with_extra_hashes_and_spaces(self):
        md = "#   Hello World   "
        self.assertEqual(extract_title(md), "Hello World")

    def test_multiple_lines_with_title_first(self):
        md = "# Heading\nSome content\nMore content"
        self.assertEqual(extract_title(md), "Heading")

    def test_multiple_lines_with_title_later(self):
        md = "Intro\n# My Title\nBody text"
        self.assertEqual(extract_title(md), "My Title")

    def test_ignores_hash_without_space(self):
        md = "#Title\n##Subtitle"
        with self.assertRaises(Exception) as cm:
            extract_title(md)
        self.assertIn("No title header", str(cm.exception))

    def test_ignores_nested_headers(self):
        md = "## Subheading\n### Another"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_no_header_raises_exception(self):
        md = "plain text only"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_empty_string_raises_exception(self):
        with self.assertRaises(Exception):
            extract_title("")

    def test_header_with_special_characters(self):
        md = "# My *Fancy* Title!"
        self.assertEqual(extract_title(md), "My *Fancy* Title!")

    def test_multiple_valid_headers_returns_first(self):
        md = "# First\n# Second\n# Third"
        self.assertEqual(extract_title(md), "First")


if __name__ == "__main__":
    unittest.main()