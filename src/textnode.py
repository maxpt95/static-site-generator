"""
This module contains representations of Markdown text, a way of conversion to HTML nodes.
"""

from __future__ import annotations

from enum import StrEnum
from typing import Any

from src.htmlnode import LeafNode


class TextType(StrEnum):
    """Sum Type for inline text elements."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    """Abstraction for Markdown text.

    Args:
        text: The text content of the node.
        text_type: The type of the text (e.g., bold, italic).
        url: Optional URL for links and images.
    """

    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other: Any) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            url = "" if text_node.url is None else text_node.url
            return LeafNode("a", text_node.text, {"href": url})
        case TextType.IMAGE:
            url = "" if text_node.url is None else text_node.url
            return LeafNode("img", "", props={"src": url, "alt": text_node.text})
        case _:
            raise ValueError(
                f"TextNode is not of a known TextType: {text_node.text_type}"
            )
