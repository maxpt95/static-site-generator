import unittest

from src.generate_site import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        markdown = """
This is some markdown

# With a title

and some other content
"""
        title = extract_title(markdown)
        self.assertEqual("With a title", title)

    def test_extract_title_no_title(self):
        with self.assertRaisesRegex(
            ValueError, "markdown must contain a level 1 header"
        ):
            extract_title("there is not title here")

    def test_eq_double(self):
        actual = extract_title(
            """
# This is a title

# This is a second title that should be ignored
"""
        )
        self.assertEqual(actual, "This is a title")

    def test_eq_long(self):
        actual = extract_title(
            """
# title

this is a bunch

of text

- and
- a
- list
"""
        )
        self.assertEqual(actual, "title")


if __name__ == "__main__":
    unittest.main()
