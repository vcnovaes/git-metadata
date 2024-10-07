"""Module for run on terminal"""

import subprocess
import fire
from entities.files_ds import FileTree
from entities.git_change import GitChange


def generate_changes_tree(repository: str, start_dir: str):
    """Main application function"""
    change_list = reversed(git_changes(repository, start_dir))
    tree = FileTree(start_dir)
    for change in change_list:
        if change.type == "A":
            tree.add_file(change.filepath)
        if change.type == "M":
            tree.register_modification(change.filepath)
        if change.type == "D":
            tree.delete_file(change.filepath)
    tree.print()


if __name__ == "__main__":
    fire.Fire(generate_changes_tree)
