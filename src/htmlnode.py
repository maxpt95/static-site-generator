"""
Representations of HTML nodes document tree.
It can be block level or inline.
"""

from __future__ import annotations


class HTMLNode:
    """Abstraction of an HTML node.

    Args:
        tag: HTML tag name (e.g., 'div', 'p', 'span').
        value: content of the node.
        children: a list of childs of the node.
        props: a dictionary containing the attributes of the node,
            where the key is the attribute name and the value its content.
    """

    def __init__(
        self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str, str] | None = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self) -> str:
        raise NotImplementedError

    def props_to_html(self) -> str:
        """Convert node attributes to an html string"""
        if not self.props:
            return ""

        html_str = ""
        for k, v in self.props.items():
            html_str += f' {k}="{v}"'

        return html_str

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    """A node with no children.

    Args:
        tag: HTML tag name (e.g., 'div', 'p', 'span'). If None, node is raw text.
        value: content of the node.
        props: a dictionary containing the attributes of the node,
            where the key is the attribute name and the value its content.
    """

    def __init__(
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self) -> str:
        """Renders leaf node as an HTML string."""
        if self.value is None:
            raise ValueError("Value can't be None.")

        if self.tag is None:
            return self.value

        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self) -> str:
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
