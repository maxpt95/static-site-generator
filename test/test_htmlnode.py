import unittest

from src.htmlnode import HTMLNode


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

        expected = 'rel="stylesheet" href="/styles.css"'

        self.assertEqual(node.props_to_html(), expected)

    def test_props_to_html_no_props(self):
        node = HTMLNode()

        self.assertEqual(node.props_to_html(), "")

    def test_to_html(self):
        self.assertRaises(NotImplementedError, HTMLNode().to_html)


if __name__ == "__main__":
    unittest.main()
