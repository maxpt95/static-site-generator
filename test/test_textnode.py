import unittest

from src.textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_url(self):
        """Test nodes are eaqual with all attributes set."""
        node = TextNode(
            "This is a text node", TextType.BOLD, "https://www.boldeagle.com"
        )
        node2 = TextNode(
            "This is a text node", TextType.BOLD, "https://www.boldeagle.com"
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


if __name__ == "__main__":
    unittest.main()
