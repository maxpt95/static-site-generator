import unittest

from src.inline_markdown import split_nodes_delimiter, extract_markdown_images
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def setUp(self) -> None:
        self.text_node = TextNode(
            "This is a text node with *bold* words in it, also `code`, *surprise *another bold",
            TextType.TEXT,
        )

    def test_no_delimiter(self):
        """Test what happens with a Falsy delimiter"""
        new_nodes = split_nodes_delimiter([self.text_node], "", TextType.BOLD)
        self.assertEqual(new_nodes, [self.text_node])

    def test_bad_text_type(self):
        """Test with a unknown TextType"""
        with self.assertRaisesRegex(ValueError, r"Given text type is unknown"):
            split_nodes_delimiter([self.text_node], "_", "UNKNOWN")  # pyright: ignore reportArgumentType

    def test_delimiter_not_found(self):
        """Test that an error is raised when a delimiter is not found in a node"""
        node = TextNode("Plain", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, r"does not contain delimiter"):
            split_nodes_delimiter([node], "*", TextType.BOLD)

    def test_split_nodes(self):
        """Test all nodes are split by the given delimiter"""
        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        text_node2 = TextNode(
            "Some *bold* text. *Pay attentiont!*",
            TextType.TEXT,
        )
        nodes = [self.text_node, italic_node, text_node2]

        new_nodes = split_nodes_delimiter(nodes, "*", TextType.BOLD)
        expected = [
            TextNode("This is a text node with ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" words in it, also `code`, ", TextType.TEXT),
            TextNode("surprise ", TextType.BOLD),
            TextNode("another bold", TextType.TEXT),
            # Second split
            TextNode("This is an italic node", TextType.ITALIC),
            # Third split
            TextNode("Some ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" text. ", TextType.TEXT),
            TextNode("Pay attentiont!", TextType.BOLD),
        ]

        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_empty_text(self):
        result = extract_markdown_images("")

        self.assertEqual(result, [])

    def test_extract(self):
        text = "This is text with an ![very important gif](https://i.imgur.com/aKaOqIh.gif) and ![pugs](https://imgur.com/gallery/blep-blep-blep-blep-JRrbFsd#HQpYUgg)"
        result = extract_markdown_images(text)

        expected = [
            ("very important gif", "https://i.imgur.com/aKaOqIh.gif"),
            ("pugs", "https://imgur.com/gallery/blep-blep-blep-blep-JRrbFsd#HQpYUgg"),
        ]
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
