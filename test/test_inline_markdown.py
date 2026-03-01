import unittest

from src.inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from src.textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def setUp(self) -> None:
        self.text_node = TextNode(
            "This is a text node with **bold** words in it, also `code`, **surprise **another bold",
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
        node = TextNode("Plain *something", TextType.TEXT)
        with self.assertRaisesRegex(ValueError, r"formatted section not closed"):
            split_nodes_delimiter([node], "*", TextType.BOLD)

    def test_split_nodes(self):
        """Test all nodes are split by the given delimiter"""
        italic_node = TextNode("This is an italic node", TextType.ITALIC)
        text_node2 = TextNode(
            "Some **bold** text. **Pay attentiont!**",
            TextType.TEXT,
        )
        nodes = [self.text_node, italic_node, text_node2]

        new_nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
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
        text = "This is text with a ![very important gif](https://i.imgur.com/aKaOqIh.gif) and ![pugs](https://i.imgur.com/HQpYUgg.jpeg)"
        result = extract_markdown_images(text)

        expected = [
            ("very important gif", "https://i.imgur.com/aKaOqIh.gif"),
            ("pugs", "https://i.imgur.com/HQpYUgg.jpeg"),
        ]
        self.assertEqual(result, expected)

    def test_dont_extract_links(self):
        text = "This is text wit a link to a [very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and ![pugs](https://i.imgur.com/HQpYUgg.jpeg)"
        result = extract_markdown_images(text)

        expected = [
            ("pugs", "https://i.imgur.com/HQpYUgg.jpeg"),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesImage(unittest.TestCase):
    def test_no_old_nodes(self):
        """Test no nodes return no nodes"""
        new_nodes = split_nodes_image([])
        self.assertEqual(new_nodes, [])

    def test_not_text_type(self):
        """Test that if a node is not TextType text it appends it as is"""
        node = TextNode(
            "This *bold* text",
            TextType.BOLD,
        )

        result = split_nodes_image([node])
        self.assertEqual([node], result)

    def test_image_not_found(self):
        """Test that if the node doesn't contain an image it will be inserted in returned list as is."""
        node = TextNode(
            "This is plain text",
            TextType.TEXT,
        )

        result = split_nodes_image([node])
        self.assertEqual([node], result)

    def test_split_nodes(self):
        """Test all nodes are split by image"""
        node1 = TextNode(
            "This is text with a link to a [very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and ![pugs](https://i.imgur.com/HQpYUgg.jpeg)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text with a ![very important gif](https://i.imgur.com/aKaOqIh.gif), and some more text",
            TextType.TEXT,
        )
        nodes = [node1, node2]

        new_nodes = split_nodes_image(nodes)
        expected = [
            TextNode(
                "This is text with a link to a [very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and ",
                TextType.TEXT,
            ),
            TextNode("pugs", TextType.IMAGE, "https://i.imgur.com/HQpYUgg.jpeg"),
            # Scond split
            TextNode("This is text with a ", TextType.TEXT),
            TextNode(
                "very important gif", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"
            ),
            TextNode(", and some more text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_empty_text(self):
        result = extract_markdown_links("")

        self.assertEqual(result, [])

    def test_extract(self):
        text = "This is text wit a link to a [very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and [pugs](https://www.youtube.com/shorts/UB2NXEHNNhw)"
        result = extract_markdown_links(text)

        expected = [
            ("very important video", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
            ("pugs", "https://www.youtube.com/shorts/UB2NXEHNNhw"),
        ]
        self.assertEqual(result, expected)

    def test_dont_extract_links(self):
        text = "This is text wit a link to a [very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ) and ![pugs](https://i.imgur.com/HQpYUgg.jpeg)"
        result = extract_markdown_links(text)

        expected = [
            ("very important video", "https://www.youtube.com/watch?v=dQw4w9WgXcQ"),
        ]
        self.assertEqual(result, expected)


class TestSplitNodesLink(unittest.TestCase):
    def test_no_old_nodes(self):
        """Test no nodes return no nodes"""
        new_nodes = split_nodes_link([])
        self.assertEqual(new_nodes, [])

    def test_not_text_type(self):
        """Test that if a node is not TextType text it appends it as is"""
        node = TextNode(
            "This *bold* text",
            TextType.BOLD,
        )

        result = split_nodes_link([node])
        self.assertEqual([node], result)

    def test_link_not_found(self):
        """Test that if the node doesn't contain an link it will be inserted in returned list as is."""
        node = TextNode(
            "This is plain text",
            TextType.TEXT,
        )

        result = split_nodes_link([node])
        self.assertEqual([node], result)

    def test_split_nodes(self):
        """Test all nodes are split by image"""
        node1 = TextNode(
            "This is text with a ![pugs](https://i.imgur.com/HQpYUgg.jpeg) image and a link to a [very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)",
            TextType.TEXT,
        )
        node2 = TextNode(
            "This is text to a [pugs](https://www.youtube.com/shorts/UB2NXEHNNhw) video, and some more text",
            TextType.TEXT,
        )
        nodes = [node1, node2]

        new_nodes = split_nodes_link(nodes)
        expected = [
            TextNode(
                "This is text with a ![pugs](https://i.imgur.com/HQpYUgg.jpeg) image and a link to a ",
                TextType.TEXT,
            ),
            TextNode(
                "very important video",
                TextType.LINK,
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            ),
            # Scond split
            TextNode("This is text to a ", TextType.TEXT),
            TextNode(
                "pugs", TextType.LINK, "https://www.youtube.com/shorts/UB2NXEHNNhw"
            ),
            TextNode(" video, and some more text", TextType.TEXT),
        ]

        self.assertEqual(new_nodes, expected)


class TestTextToTextNodes(unittest.TestCase):
    def test_to_text_nodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and a ![pugs image](https://i.imgur.com/HQpYUgg.jpeg) and a [link to a very important video](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"

        nodes = text_to_textnodes(text)

        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and a ", TextType.TEXT),
            TextNode("pugs image", TextType.IMAGE, "https://i.imgur.com/HQpYUgg.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode(
                "link to a very important video",
                TextType.LINK,
                "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            ),
        ]

        self.assertEqual(nodes, expected)


if __name__ == "__main__":
    unittest.main()
