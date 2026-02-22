import unittest

from src.htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(
            "div", [child_node], {"first": "attr value", "second": "2nd value"}
        )
        self.assertEqual(
            parent_node.to_html(),
            '<div first="attr value" second="2nd value"><span>child</span></div>',
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("", [child_node])

        self.assertRaises(ValueError, parent_node.to_html)

    def test_to_html_no_children(self):
        parent_node = ParentNode("div", [])

        self.assertRaises(ValueError, parent_node.to_html)

    def test_repr(self):
        child_node = LeafNode("span", "child")
        props = {"attr": "attr value"}
        parent_node = ParentNode("div", [child_node], props)
        # child node representation is handled child itself
        expected = f"ParentNode(div, children: [{child_node}], {props})"
        self.assertEqual(str(parent_node), expected)


if __name__ == "__main__":
    unittest.main()
