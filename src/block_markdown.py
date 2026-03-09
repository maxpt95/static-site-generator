from enum import StrEnum

import re


class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Splits makrdown text blocks into a list."""
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]


def block_to_block_type(markdown: str) -> BlockType:
    """Determines the BlockType of a markdown block."""
    if markdown.startswith("#"):
        return BlockType.HEADING
    elif markdown.startswith("```"):
        return BlockType.CODE

    lines = markdown.splitlines()
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.UNORDERED_LIST
    elif all(re.match(r"^\d*\. ", line) is not None for line in lines):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
