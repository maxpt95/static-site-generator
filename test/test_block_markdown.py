import unittest
from src.block_markdown import markdown_to_blocks, block_to_block_type, BlockType


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
        self.assertEqual(block_to_block_type(markdown), BlockType.UNORDERED_LIST)

    def test_to_unordered_list_no_space(self):
        markdown = """-This is a list
-with items
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.PARAGRAPH)

    def test_to_ordered_list(self):
        markdown = """1. This is a list
2. with items
"""
        self.assertEqual(block_to_block_type(markdown), BlockType.ORDERED_LIST)

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


if __name__ == "__main__":
    unittest.main()
