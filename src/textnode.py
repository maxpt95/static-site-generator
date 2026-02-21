"""This module contains representations of HTML inline texts."""

from __future__ import annotations

from enum import StrEnum
from typing import Any


class TextType(StrEnum):
    """Sum Type for inline text elements."""

    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "links"
    IMAGES = "images"


class TextNode:
    """Abstraction for HTML inline text elements.

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
