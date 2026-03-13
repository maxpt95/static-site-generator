import unittest

from src.block_markdown import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_to_heading(self):
        self.assertEqual(block_to_block_type("# Title 1"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("## Title 2"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("### Title 3"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("#### Title 4"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("##### Title 5"), BlockType.HEADING)
        self.assertEqual(block_to_block_type("###### Title 6"), BlockType.HEADING)

    def test_to_heading_no_space(self):
        self.assertEqual(block_to_block_type("#not a heading"), BlockType.PARAGRAPH)

    def test_to_code(self):
        markdown = """```
code block
```"""
        self.assertEqual(block_to_block_type(markdown), BlockType.CODE)

    def test_to_code_not_code(self):
        self.assertEqual(block_to_block_type("```code block```"), BlockType.PARAGRAPH)

        not_block_code = """```
some code
"""
        self.assertEqual(block_to_block_type(not_block_code), BlockType.PARAGRAPH)

    def test_to_quote(self):
        markdown = """> This is a quote
>with multiple lines
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.QUOTE)

    def test_to_unordered_list(self):
        markdown = """- This is a list
- with items
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.ULIST)

    def test_to_unordered_list_no_space(self):
        markdown = """-This is a list
-with items
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_to_ordered_list(self):
        markdown = """1. This is a list
2. with items
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.OLIST)

    def test_to_ordered_list_no_space(self):
        markdown = """1.This is a list
2.with items
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_to_paragraph(self):
        markdown = """This is a paragraph
with multiple lines
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()
