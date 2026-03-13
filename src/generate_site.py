from src.block_markdown import markdown_to_html_node
import os


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating {dest_path} from {template_path} and {from_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_html = template.format(title=title, content=html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    with open(dest_path, "w") as f:
        f.write(page_html)


def extract_title(markdown: str) -> str:
    """Extracts the title from the first level 1 header in a markdown."""
    header_i = markdown.find("# ")
    if header_i == -1:
        raise ValueError("markdown must contain a level 1 header")

    markdown_from_title = markdown[header_i + 2 :]
    return markdown_from_title[: markdown_from_title.find("\n")]
