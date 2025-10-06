import unittest

from markdown_to_blocks import markdown_to_blocks

class TestMarkdownToBlocks(unittest.TestCase):

    def test_empty_doc(self):
        doc = ""
        self.assertEqual(markdown_to_blocks(doc), [])

    def test_single_block(self):
        doc = "This is a single block"
        self.assertEqual(markdown_to_blocks(doc), ["This is a single block"])

    def test_multiple_blocks(self):
        doc = "Block one\n\nBlock two\n\nBlock three"
        expected = ["Block one", "Block two", "Block three"]
        self.assertEqual(markdown_to_blocks(doc), expected)

    def test_blocks_with_extra_whitespace(self):
        doc = "   Block one   \n\n   Block two   "
        expected = ["Block one", "Block two"]
        self.assertEqual(markdown_to_blocks(doc), expected)

    def test_ignores_empty_splits(self):
        doc = "Block one\n\n\n\nBlock two"
        expected = ["Block one", "Block two"]
        self.assertEqual(markdown_to_blocks(doc), expected)

    def test_trailing_newlines(self):
        doc = "Block one\n\nBlock two\n\n"
        expected = ["Block one", "Block two"]
        self.assertEqual(markdown_to_blocks(doc), expected)

    
    def test_start_with_newlines(self):
        doc = "\n\n\n\n\n\n\n\n\n\nBlock one\n\nBlock two\n\n"
        expected = ["Block one", "Block two"]
        self.assertEqual(markdown_to_blocks(doc), expected)

    def test_end_with_newlines(self):
        doc = "\n\nBlock one\n\nBlock two\n\n\n\n\n\n\n\n\n\n\n\n\n\n"
        expected = ["Block one", "Block two"]
        self.assertEqual(markdown_to_blocks(doc), expected)

if __name__ == "__main__":
    unittest.main()