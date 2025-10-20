import unittest

from extract_img_and_links import extract_markdown_images, extract_markdown_links

class TestExtractLinksAndImages(unittest.TestCase):

    def test_extract_images(self):
        matches = extract_markdown_images(
        "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches = extract_markdown_images(
        "![dexter](https://cdn.hanna-barberawiki.com/thumb/8/82/Dexter.jpg/300px-Dexter.jpg)"
        )
        self.assertListEqual([("dexter", "https://cdn.hanna-barberawiki.com/thumb/8/82/Dexter.jpg/300px-Dexter.jpg")], matches)

        matches = extract_markdown_images(
        "![]()"
        )
        self.assertListEqual([("", "")], matches)

        matches = extract_markdown_images(
        "![apple](https://www.applesfromny.com/wp-content/uploads/2020/06/SnapdragonNEW.png) and ![apple](https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg)"
        )
        self.assertListEqual([("apple", "https://www.applesfromny.com/wp-content/uploads/2020/06/SnapdragonNEW.png"),("apple","https://upload.wikimedia.org/wikipedia/commons/f/fa/Apple_logo_black.svg")], matches)

    def test_extract_images_none(self):
        matches = extract_markdown_images(
        "![]("
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
        "[]()"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
        "!"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_images(
        "![test])"
        )
        self.assertListEqual([], matches)

    def test_extract_links(self):
        matches = extract_markdown_links(
        "This is text with an [google](https://www.google.com/)"
        )
        self.assertListEqual([("google", "https://www.google.com/")], matches)

        matches = extract_markdown_links(
        "[dexter](https://cdn.hanna-barberawiki.com/thumb/8/82/Dexter.jpg/300px-Dexter.jpg)"
        )
        self.assertListEqual([("dexter", "https://cdn.hanna-barberawiki.com/thumb/8/82/Dexter.jpg/300px-Dexter.jpg")], matches)

        matches = extract_markdown_links(
        "[]()"
        )
        self.assertListEqual([("", "")], matches)

        matches = extract_markdown_links(
        "[boot](https://www.boot.dev/dashboard) and [boot](https://www.boot.dev/dashboard)"
        )
        self.assertListEqual([("boot", "https://www.boot.dev/dashboard"),("boot","https://www.boot.dev/dashboard")], matches)

    def test_extract_links_none(self):
        matches = extract_markdown_links(
        "[]("
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
        "[()"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
        "!"
        )
        self.assertListEqual([], matches)

        matches = extract_markdown_links(
        "[test])"
        )
        self.assertListEqual([], matches)
        
        matches = extract_markdown_links(
        "![test]()"
        )
        self.assertListEqual([], matches)