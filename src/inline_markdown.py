import re

from src.textnode import TextNode, TextType


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    """Splits TextNodes into multiple nodes based on the delimiters.

    Non TEXT nodes will be added to the splited list as is.

    Args:
        old_nodes: a list of TextNodes to split.
        delimiter: the string to look for when spliting.
        text_type: the TextType of the resulting nodes.
    Raises:
        ValueError:
            - when given an unknown text type.
            - when the delimiter is not found in one of the old nodes.
    Returns:
        A list of the nodes splited from the old nodes.
    """
    if not delimiter:
        return old_nodes

    if text_type not in TextType:
        raise ValueError(f"Given text type is unknown: {text_type}")

    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_text = node.text.split(delimiter)

        if len(split_text) == 1:
            raise ValueError(
                f"Old node text '{node.text}' does not contain delimiter: {delimiter}"
            )

        for i, txt in enumerate(split_text):
            if txt == "":
                continue
            new_text_type = text_type if i % 2 != 0 else TextType.TEXT
            new_node = TextNode(txt, new_text_type)
            new_nodes.append(new_node)

    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split a list of TextNodes by its image markdown text.

    Non TEXT nodes will be added to the splited list as is.

    Args:
        old_nodes: a list of TextNodes to split.
    Raises:
        ValueError:
            - when the node does not contain an image.
    Returns:
        A list of the nodes splited from the old nodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        image_text_pairs = extract_markdown_images(node.text)

        if not len(image_text_pairs):
            new_nodes.append(node)
            continue

        text_to_split = node.text
        for alt_text, url in image_text_pairs:
            splited_text = text_to_split.split(f"![{alt_text}]({url})", 1)
            if splited_text[0] != "":
                new_nodes.append(TextNode(splited_text[0], node.text_type))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, url))
            text_to_split = splited_text[1]

        # Add remaining text if the last string in the text wasn't an image.
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, node.text_type))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    """Split a list of TextNodes by its link markdown text.

    Non TEXT nodes will be added to the splited list as is.

    Args:
        old_nodes: a list of TextNodes to split.
    Raises:
        ValueError:
            - when the node does not contain an image.
    Returns:
        A list of the nodes splited from the old nodes.
    """
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        link_text_pairs = extract_markdown_links(node.text)

        if not len(link_text_pairs):
            new_nodes.append(node)
            continue

        text_to_split = node.text
        for anchor, url in link_text_pairs:
            splited_text = text_to_split.split(f"[{anchor}]({url})", 1)
            if splited_text[0] != "":
                new_nodes.append(TextNode(splited_text[0], node.text_type))
            new_nodes.append(TextNode(anchor, TextType.LINK, url))
            text_to_split = splited_text[1]

        # Add remaining text if the last string in the text wasn't a link.
        if text_to_split != "":
            new_nodes.append(TextNode(text_to_split, node.text_type))

    return new_nodes


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    """Extracts image information from raw markdown text.

    Args:
        text: markdown text to extract the image info from.
    Return:
        A list of tuples. Each tuple contains the alternative text
        of the image and its url.
    """
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    """Extracts links information from raw markdown text.

    Args:
        text: markdown text to extract the link info from.
    Return:
        A list of tuples. Each tuple contains the anchor text
        of the link and its url.
    """
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
