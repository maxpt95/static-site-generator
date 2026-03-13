import re
from enum import StrEnum

from src.htmlnode import ParentNode, LeafNode
from src.inline_markdown import text_to_textnodes
from src.textnode import TextNode, TextType, text_node_to_html_node


class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    """Splits makrdown text blocks into a list."""
    return [block.strip() for block in markdown.split("\n\n") if block.strip() != ""]


def block_to_block_type(markdown: str) -> BlockType:
    """Determines the BlockType of a markdown block."""
    if re.match(r"^#{1,6} ", markdown) is not None:
        return BlockType.HEADING
    elif markdown.startswith("```\n") and markdown.endswith("```"):
        return BlockType.CODE

    lines = markdown.splitlines()
    if all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith("- ") for line in lines):
        return BlockType.ULIST
    elif all(line.startswith(f"{i + 1}. ") for i, line in enumerate(lines)):
        return BlockType.OLIST
    return BlockType.PARAGRAPH


def markdown_to_html_node(markdown: str) -> ParentNode:
    """Converts a markdown string into an HTMLNode."""
    blocks = markdown_to_blocks(markdown)

    block_html_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)

        match block_type:
            case BlockType.HEADING:
                block_node = heading_block_to_html_node(block)
            case BlockType.CODE:
                block_node = code_block_to_html_node(block)
            case BlockType.QUOTE:
                block_node = quote_block_to_html_node(block)
            case BlockType.ULIST:
                block_node = ulist_block_to_html_node(block)
            case BlockType.OLIST:
                block_node = olist_block_to_html_node(block)
            case BlockType.PARAGRAPH:
                block_node = paragraph_block_to_html_node(block)

        block_html_nodes.append(block_node)

    return ParentNode("div", block_html_nodes)


def text_to_children(text: str) -> list[LeafNode]:
    """Converts a string into a list of childnodes representing the inline markdown."""
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]


def heading_block_to_html_node(block: str) -> ParentNode:
    """Converts a heading block into an HTML node."""
    header_match = re.match(r"^#{1,6}", block)
    if header_match is None:
        raise ValueError(f"Invalid header: {block}")
    header_num = len(header_match[0])
    # Slice header removing "#" symbols and the white space.
    text = block[header_num + 1 :]
    child_nodes = text_to_children(text)

    return ParentNode(f"h{header_num}", child_nodes)


def code_block_to_html_node(block: str) -> ParentNode:
    """Converts a code block into an HTML node."""
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block.")
    # A code block should be inside of a pre block. E.g <pre><code></pre></code>
    tag = "pre"
    text_node = TextNode(block.split("```")[1][1:], TextType.CODE)
    child_nodes = [text_node_to_html_node(text_node)]
    return ParentNode(tag, child_nodes)


def quote_block_to_html_node(block: str) -> ParentNode:
    """Converts a quote block into an HTML node."""
    tag = "blockquote"

    new_lines = []
    for line in block.splitlines():
        if not line.startswith(">"):
            raise ValueError("Invalid quote block")
        new_lines.append(line.lstrip(">").strip())

    child_nodes = text_to_children(" ".join(new_lines))

    return ParentNode(tag, child_nodes)


def ulist_block_to_html_node(block: str) -> ParentNode:
    """Convert an unordered list block into an HTML node."""
    list_nodes = []
    for line in block.splitlines():
        # Slice quote lines removing the list symbol and white space.
        children = text_to_children(line[2:])
        li_node = ParentNode("li", children)
        list_nodes.append(li_node)

    return ParentNode("ul", list_nodes)


def olist_block_to_html_node(block: str) -> ParentNode:
    """Convert an ordered list block into an HTML node."""
    list_nodes = []
    for line in block.splitlines():
        children = text_to_children(line.split(". ", maxsplit=1)[1])
        li_node = ParentNode("li", children)
        list_nodes.append(li_node)

    return ParentNode("ol", list_nodes)


def paragraph_block_to_html_node(block: str) -> ParentNode:
    """Convert a paragraph block into an HTML node."""
    children = text_to_children(block.replace("\n", " "))
    return ParentNode("p", children)
