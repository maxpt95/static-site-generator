from src.block_markdown import markdown_to_html_node
import os


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"- {from_path} -> {dest_path}")

    with open(from_path, "r") as f:
        markdown = f.read()
    with open(template_path, "r") as f:
        template = f.read()

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page_html = template.replace("{{title}}", title).replace("{{content}}", html)

    dest_dir = os.path.dirname(dest_path)
    if not os.path.exists(dest_dir):
        os.mkdir(dest_dir)

    with open(dest_path, "w") as f:
        f.write(page_html)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    print(f"Generating pages from {dir_path_content} into {dest_dir_path}...")
    if not os.path.isdir(dir_path_content):
        raise ValueError("content path must point to a directory")

    for og_name in os.listdir(dir_path_content):
        og_path = os.path.join(dir_path_content, og_name)
        if os.path.isfile(og_path):
            html_name = f"{os.path.basename(og_path).split('.')[0]}.html"
            html_path = os.path.join(dest_dir_path, html_name)
            generate_page(og_path, template_path, html_path)
        else:
            dest_path = os.path.join(dest_dir_path, og_name)
            if not os.path.exists(dest_path):
                os.mkdir(dest_path)
            generate_pages_recursive(og_path, template_path, dest_path)


def extract_title(markdown: str) -> str:
    """Extracts the title from the first level 1 header in a markdown."""
    header_i = markdown.find("# ")
    if header_i == -1:
        raise ValueError("markdown must contain a level 1 header")

    markdown_from_title = markdown[header_i + 2 :]
    return markdown_from_title[: markdown_from_title.find("\n")]
