import unittest

from src.htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        child_node = HTMLNode(
            "link", props={"rel": "stylesheet", "href": "/styles.css"}
        )
        node = HTMLNode("head", "text", [child_node])

        expected = "HTMLNode(head, text, [HTMLNode(link, None, None, {'rel': 'stylesheet', 'href': '/styles.css'})], None)"

        self.assertEqual(str(node), expected)

    def test_props_to_html(self):
        node = HTMLNode("link", props={"rel": "stylesheet", "href": "/styles.css"})

        expected = ' rel="stylesheet" href="/styles.css"'

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        self.assertRaises(NotImplementedError, HTMLNode().to_html)


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_props(self):
        node = LeafNode(
            "a", "Click me! please ;)", {"href": "https://www.not-phishing.com"}
        )

        expected = '<a href="https://www.not-phishing.com">Click me! please ;)</a>'
        self.assertEqual(node.to_html(), expected)

    def test_to_html_no_value(self):
        node = LeafNode("p", value=None)  # pyright: ignore[reportArgumentType]

        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_tag(self):
        node = LeafNode(None, "no tag")

        self.assertEqual(node.to_html(), "no tag")

    def test_repr(self):
        props = {"href": "https://www.not-phishing.com"}
        node = LeafNode("a", "Click me! please ;)", props)

        expected = f"LeafNode(a, Click me! please ;), {props})"
        self.assertEqual(str(node), expected)


if __name__ == "__main__":
    unittest.main()
