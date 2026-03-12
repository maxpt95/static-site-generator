"""
Manages publication of static files.

We don't use shushutil.copytree because it easy.
"""

import os
import shutil


def copy_dir_recursive(og_dir_path: str, dest_dir_path: str) -> None:
    """Recursively copy the contents of a directory to another."""
    if os.path.isfile(og_dir_path):
        raise ValueError("original path must be a directory")

    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for element_name in os.listdir(og_dir_path):
        og_path = os.path.join(og_dir_path, element_name)
        dest_path = os.path.join(dest_dir_path, element_name)
        print(f"- {og_path} -> {dest_path}")
        if os.path.isfile(og_path):
            shutil.copy(og_path, dest_path)
        else:
            copy_dir_recursive(og_path, dest_path)
