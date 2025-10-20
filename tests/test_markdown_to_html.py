import unittest
import re

from markdown_to_html_node import markdown_to_html_node, get_header_tag

def normalize_html(s: str) -> str:
    # Collapse whitespace between tags and strip outer spaces
    s = re.sub(r">\s+<", "><", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

class TestMarkdownToHtmlNode(unittest.TestCase):
    def assertHtmlEqual(self, actual: str, expected: str):
        self.assertEqual(normalize_html(actual), normalize_html(expected))

    def test_paragraph_simple(self):
        md = "Hello world"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(html, "<div><p>Hello world</p></div>")

    def test_header_h2(self):
        md = "## Hello"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(html, "<div><h2>Hello</h2></div>")

    def test_code_block_fenced_inline_single_line(self):
        # Using inline fence to avoid newline edge cases from .strip('```')
        md = "```print(1)```"
        html = markdown_to_html_node(md).to_html()
        # Only check structure and core content
        self.assertIn("<pre>", html)
        self.assertIn("<code>", html)
        self.assertIn("print(1)", html)
        self.assertIn("</code>", html)
        self.assertIn("</pre>", html)

    def test_blockquote_single_paragraph(self):
        md = "> Life is like riding a bicycle."
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(
            html,
            "<div><blockquote><p>Life is like riding a bicycle.</p></blockquote></div>",
        )

    def test_blockquote_multiple_paragraphs(self):
        md = (
            "> First line of quote\n"
            ">\n"
            "> Second paragraph of quote"
        )
        html = markdown_to_html_node(md).to_html()
        # Expect two paragraphs inside the blockquote
        self.assertIn("<blockquote>", html)
        self.assertIn("<p>First line of quote</p>", html)
        self.assertIn("<p>Second paragraph of quote</p>", html)

    def test_unordered_list(self):
        md = "- a\n- b\n- c"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(
            html,
            "<div><ul><li>a</li><li>b</li><li>c</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. alpha\n2. beta\n3. gamma"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(
            html,
            "<div><ol><li>alpha</li><li>beta</li><li>gamma</li></ol></div>",
        )

    def test_mixed_document(self):
        md = (
            "## Title\n\n"
            "Paragraph text here.\n\n"
            "- one\n- two\n\n"
            "1. first\n2. second\n\n"
            "> quoted\n\n"
            "```code```"
        )
        html = markdown_to_html_node(md).to_html()
        # Spot-check presence and order of key sections
        # Title
        self.assertRegex(html, r"<h2>Title</h2>")
        # Paragraph
        self.assertRegex(html, r"<p>Paragraph text here\.</p>")
        # UL
        self.assertRegex(html, r"<ul>.*<li>one</li>.*<li>two</li>.*</ul>")
        # OL
        self.assertRegex(html, r"<ol>.*<li>first</li>.*<li>second</li>.*</ol>")
        # Blockquote
        self.assertRegex(html, r"<blockquote>.*<p>quoted</p>.*</blockquote>")
        # Code
        self.assertIn("<pre>", html)
        self.assertIn("<code>code</code>", html)

class TestGetHeaderTag(unittest.TestCase):
    def test_header_tags_by_space_index(self):
        # get_header_tag uses index of first space as the level
        self.assertEqual(get_header_tag("# H1"), "h1")
        self.assertEqual(get_header_tag("## Heading"), "h2")
        self.assertEqual(get_header_tag("### Title"), "h3")
        self.assertEqual(get_header_tag("###### Deep"), "h6")

    def test_header_tag_missing_space(self):
        # If no space exists, .find(' ') returns -1; decide what you expect.
        # You may want to define desired behavior; here we assert current behavior.
        self.assertEqual(get_header_tag("####NoSpace"), "h-1")

class TestMarkdownToHtmlNodeEdgeCases(unittest.TestCase):
    def assertHtmlEqual(self, actual: str, expected: str):
        self.assertEqual(normalize_html(actual), normalize_html(expected))

    # ---------- Empty & whitespace-only ----------
    def test_empty_input_returns_empty_div(self):
        md = ""
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(html, "<div></div>")

    def test_whitespace_only(self):
        md = "   \n  \n"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(html, "<div></div>")

    # ---------- Headers ----------
    def test_header_without_space(self):
        # Documents current behavior of get_header_tag when there is no space
        self.assertEqual(get_header_tag("###NoSpace"), "h-1")

    # ---------- Blockquotes ----------
    def test_blockquote_with_no_space_after_arrow(self):
        md = ">Quoted with no leading space"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(
            html,
            "<div><blockquote><p>Quoted with no leading space</p></blockquote></div>"
        )

    def test_blockquote_nested_marker_only_strips_one_level(self):
        md = ">> nested level"
        html = markdown_to_html_node(md).to_html()
        # Only one '>' stripped; remaining '>' should be visible in text content
        self.assertRegex(html, r"<blockquote>.*<p>> nested level</p>.*</blockquote>")

    # ---------- Unordered lists ----------
    def test_unordered_list_trailing_spaces_and_blank_line(self):
        md = "- a  \n- b\n\n"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(html, "<div><ul><li>a  </li><li>b</li></ul></div>")

    def test_unordered_list_dash_only_lines(self):
        # Lines that are just '-' (with a space) should render empty li bodies
        md = "- \n- item"
        html = markdown_to_html_node(md).to_html()
        self.assertIn("<ul>", html)
        self.assertIn("<li></li>", html)
        self.assertIn("<li>item</li>", html)

    # ---------- Ordered lists (numbering quirks) ----------
    def test_ordered_list_not_starting_at_one_is_preserved_in_text(self):
        md = "3. alpha\n4. beta"
        html = markdown_to_html_node(md).to_html()
        # Numbers out of order so will be paragraph
        self.assertHtmlEqual(
            html,
            "<div><p>3. alpha 4. beta</p></div>"
        )

    def test_ordered_list_misnumbered_line(self):
        md = "1. one\n3. three"
        html = markdown_to_html_node(md).to_html()
        # Second line won't match '2. ' prefix removal, so will be paragraph
        self.assertHtmlEqual(
            html,
            "<div><p>1. one 3. three</p></div>"
        )

    # ---------- Code fences ----------
    def test_fenced_code_multiline(self):
        md = "```\nprint(1)\nprint(2)\n```"
        html = markdown_to_html_node(md).to_html()
        # Structure + content check
        self.assertIn("<pre>", html)
        self.assertIn("<code>", html)
        self.assertIn("print(1)", html)
        self.assertIn("print(2)", html)

    def test_fenced_code_with_language_info_is_treated_as_content(self):
        md = "```python\nprint(1)\n```"
        html = markdown_to_html_node(md).to_html()
        # Current code strips backticks only; 'python\n' remains in the code body
        self.assertIn("<pre>", html)
        self.assertIn("<code>", html)
        self.assertIn("python", html)
        self.assertIn("print(1)", html)

    def test_inline_fence_with_backticks_inside_content(self):
        md = "```print(`tick` inside)```"
        html = markdown_to_html_node(md).to_html()
        # strip('```') removes only leading/trailing backticks; inner backticks remain
        self.assertIn("print(`tick` inside)", html)

    # ---------- Paragraph normalization ----------
    def test_paragraph_with_trailing_newlines(self):
        md = "Hello, world!\n\n"
        html = markdown_to_html_node(md).to_html()
        self.assertHtmlEqual(html, "<div><p>Hello, world!</p></div>")

    def test_multiple_paragraphs_split(self):
        md = "First paragraph.\n\nSecond paragraph."
        html = markdown_to_html_node(md).to_html()
        # Expect two <p> siblings
        self.assertRegex(html, r"<div>.*<p>First paragraph\.</p>.*<p>Second paragraph\.</p>.*</div>")

class TestGetHeaderTagEdgeCases(unittest.TestCase):
    def test_leading_hashes_then_multiple_spaces(self):
        self.assertEqual(get_header_tag("###   Title"), "h3")

    def test_only_hashes(self):
        # No space => current behavior returns h-1
        self.assertEqual(get_header_tag("######"), "h-1")

    def test_space_is_first_char(self):
        # If string starts with space, find(' ') returns 0 -> "h0"
        self.assertEqual(get_header_tag(" ### Title"), "h0")

if __name__ == "__main__":
    unittest.main()