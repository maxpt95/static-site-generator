import os
import shutil

from src.constants import CONTENT_PATH, PUBLIC_DIR_PATH, STATIC_DIR_PATH, TEMPLATE_PATH
from src.copy_static import copy_dir_recursive
from src.generate_site import generate_page


def main():
    print("Deleting public directory...")
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)

    print("Copy static dir contents into public...")
    copy_dir_recursive(STATIC_DIR_PATH, PUBLIC_DIR_PATH)

    index_path = os.path.join(CONTENT_PATH, "index.md")
    des_path = os.path.join(PUBLIC_DIR_PATH, "index.html")
    generate_page(index_path, TEMPLATE_PATH, des_path)


if __name__ == "__main__":
    main()
