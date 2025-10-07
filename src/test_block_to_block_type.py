import unittest
from block_to_block_type import block_to_block_type, is_code, is_header, is_ordered_list, is_quote, is_unordered_list, BlockType

class TestBlockDetectors(unittest.TestCase):

    # ---------- HEADER ----------
    def test_header_valid_levels_1_to_6(self):
        for n in range(1, 7):
            with self.subTest(level=n):
                self.assertTrue(is_header('#' * n + ' Heading'))

    def test_header_requires_space(self):
        self.assertFalse(is_header('#NoSpace'))
        self.assertFalse(is_header('######No space'))
        self.assertTrue(is_header('###### with space'))

    def test_header_too_many_hashes(self):
        self.assertFalse(is_header('####### too many'))

    # ---------- CODE ----------
    def test_code_single_line(self):
        self.assertTrue(is_code('```code```'))

    def test_code_multiline(self):
        block = "```\nline1\nline2()\n```"
        self.assertTrue(is_code(block))

    def test_code_must_start_and_end_with_triple_backticks(self):
        self.assertFalse(is_code('```unclosed'))
        self.assertFalse(is_code('unopened```'))
        self.assertFalse(is_code('`` not triple ```'))

    # ---------- QUOTE ----------
    def test_quote_every_line_gt(self):
        block = "> a\n> b c d\n> e"
        self.assertTrue(is_quote(block))

    def test_quote_rejects_any_line_without_gt(self):
        block = "> a\nnope\n> b"
        self.assertFalse(is_quote(block))

    def test_quote_single_line(self):
        self.assertTrue(is_quote('> just one line'))

    # ---------- UNORDERED LIST ----------
    def test_unordered_list_all_lines_dash_space(self):
        block = "- one\n- two\n- three"
        self.assertTrue(is_unordered_list(block))

    def test_unordered_list_rejects_missing_dash_or_space(self):
        self.assertFalse(is_unordered_list('— emdash not hyphen'))
        self.assertFalse(is_unordered_list('-no space'))
        self.assertFalse(is_unordered_list('- ok\nnot-a-list'))
        self.assertFalse(is_unordered_list('- ok\n-  ok (two spaces okay)'))

    def test_unordered_list_single_item(self):
        self.assertTrue(is_unordered_list('- item'))

    # ---------- ORDERED LIST ----------
    def test_ordered_list_simple_sequence(self):
        block = "1. one\n2. two\n3. three"
        self.assertTrue(is_ordered_list(block))

    def test_ordered_list_must_start_at_one(self):
        self.assertFalse(is_ordered_list('2. starts wrong'))

    def test_ordered_list_rejects_skips_or_resets(self):
        self.assertFalse(is_ordered_list('1. one\n3. three'))
        self.assertFalse(is_ordered_list('1. one\n2. two\n2. oops'))

    def test_ordered_list_zero_padded_numbers_rejected(self):
        self.assertFalse(is_ordered_list('01. zero padded\n02. still padded'))

    def test_ordered_list_single_item(self):
        self.assertTrue(is_ordered_list('1. only item'))

    # ---------- FALLBACK / PARAGRAPH ----------
    def test_paragraph_when_no_patterns_match(self):
        block = "Just a regular paragraph."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    # ---------- block_to_block_type classification ----------
    def test_block_type_header(self):
        self.assertEqual(block_to_block_type('# Title'), BlockType.HEADER)

    def test_block_type_code(self):
        self.assertEqual(block_to_block_type('```\nprint("hi")\n```'), BlockType.CODE)

    def test_block_type_quote(self):
        self.assertEqual(block_to_block_type('> q1\n> q2'), BlockType.QUOTE)

    def test_block_type_unordered_list(self):
        self.assertEqual(block_to_block_type('- a\n- b'), BlockType.UNORDERED_LIST)

    def test_block_type_ordered_list(self):
        self.assertEqual(block_to_block_type('1. a\n2. b'), BlockType.ORDERED_LIST)

    def test_block_type_priority_when_multiple_could_match(self):
        self.assertEqual(block_to_block_type('- ```not code fence start```'), BlockType.UNORDERED_LIST)

    def test_lines_with_internal_trailing_spaces_already_stripped_externally(self):
        block = "1. one  \n2. two"
        self.assertTrue(is_ordered_list(block))


if __name__ == "__main__":
    unittest.main()