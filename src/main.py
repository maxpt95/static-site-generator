import os
import shutil

from src.constants import PUBLIC_DIR_PATH, STATIC_DIR_PATH
from src.copy_static import copy_dir_recursive


def main():
    print("Deleting public directory...")
    if os.path.exists(PUBLIC_DIR_PATH):
        shutil.rmtree(PUBLIC_DIR_PATH)

    print("Copy static dir contents into public...")
    copy_dir_recursive(STATIC_DIR_PATH, PUBLIC_DIR_PATH)


if __name__ == "__main__":
    main()
