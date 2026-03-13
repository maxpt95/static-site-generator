import os
import shutil
import sys

from src.constants import CONTENT_PATH, PUBLIC_DIR_PATH, STATIC_DIR_PATH, TEMPLATE_PATH
from src.copy_static import copy_dir_recursive
from src.generate_site import generate_pages_recursive


def main():
    basepath = sys.argv[0] if len(sys.argv) > 0 else "/"

    print("Deleting public directory...")
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)

    print("Copy static dir contents into public...")
    copy_dir_recursive(STATIC_DIR_PATH, PUBLIC_DIR_PATH)

    print("Generating site...")
    generate_pages_recursive(basepath, CONTENT_PATH, TEMPLATE_PATH, PUBLIC_DIR_PATH)


if __name__ == "__main__":
    main()
