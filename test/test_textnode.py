import unittest

from src.textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        """Test nodes are eaqual with all attributes set."""
        node = TextNode(
            "This is a text node", TextType.LINK, "https://www.baldeagle.com"
        )
        node2 = TextNode(
            "This is a text node", TextType.LINK, "https://www.baldeagle.com"
        )
        self.assertEqual(node, node2)

    def test_eq_false(self):
        """Test Nodes are different if text_type is different."""
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        """Test Nodes are different if text is different."""
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a different text node", TextType.TEXT)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node_rep = str(TextNode("This is a text node", TextType.TEXT))
        expected = "TextNode(This is a text node, text, None)"
        self.assertEqual(node_rep, expected)


class TestTextNodeToHtmlNode(unittest.TestCase):
    """Test TextNode to HTML Node conversions."""

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_code(self):
        node = TextNode("This is a code node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code node")

    def test_link(self):
        node = TextNode(
            "This is a link node", TextType.LINK, "https://www.something.com"
        )
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link node")
        self.assertEqual(html_node.props, {"href": "https://www.something.com"})

    def test_image(self):
        node = TextNode("This is an image node", TextType.IMAGE, "https://some.image")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://some.image", "alt": "This is an image node"},
        )


if __name__ == "__main__":
    unittest.main()
