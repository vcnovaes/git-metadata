import subprocess
import csv
from collections import defaultdict


class FileNode:
    def __init__(self, label: str, count: int = 0, children=None) -> None:
        if children == None:
            self.children = dict()

        self.label = label
        self.count = count
        pass

    def increase_modification_count(self):
        self.count += 1

    def __str__(self) -> str:
        return f"{self.label}"

    def __repr__(self) -> str:
        return f"{self.label}.count:{self.count}"


class FileTree:
    def __init__(self, root_node_name: str) -> None:
        self.root = FileNode(root_node_name)

    def print(self, node: FileNode = None, counter=0):
        if node == None:
            node = self.root
        if "." in node.label:
            print(f"{node.label}({node.count})", end="\n")
        else:
            print(f"{node.label}({node.count})", end="/")
        if counter == 900:
            return
        if len(node.children) > 0:
            for child_node in node.children.values():
                self.print(child_node, counter + 1)

    def __find_or_create_path(self, file_path: str) -> list[FileNode]:
        path_dir_list = file_path.split("/")

        current_node = self.root
        path_nodes = [current_node]

        for directory in path_dir_list[1:]:
            if directory not in current_node.children:
                current_node.children[directory] = FileNode(directory)
            current_node = current_node.children[directory]

            path_nodes.append(current_node)
        return path_nodes

    def add_file(self, filename: str):
        # adicionar na arvore
        path_nodes = self.__find_or_create_path(filename)
        # somar count nos anteriores
        for node in path_nodes:
            node.count += 1

    def register_modification(self, filename: str):
        self.add_file(filename)

    def delete_file(self, filename: str):
        pass

    def rename_file(self, old_filename: str, new_filename: str):
        pass


class GitChange:
    def __init__(self, modification_type: str, filepath: str) -> None:
        self.type = modification_type
        self.filepath = filepath

    @staticmethod
    def from_string(raw_modification_log: str):
        try:
            change_type, filename = raw_modification_log.split("\t", 1)
            return GitChange(change_type, filename)
        except ValueError as error:
            print(f"ValueError: {error} \t {raw_modification_log} was not processed")

    def __str__(self) -> str:
        return (self.type, self.filepath)


def __raw_git_data():
    return (
        subprocess.run(
            ["git", "log", "--name-status", "--pretty=format:"], stdout=subprocess.PIPE
        )
        .stdout.decode()
        .splitlines()
    )


def git_changes(root_dir: str = "src"):
    node_changes = [
        GitChange.from_string(raw_node)
        for raw_node in __raw_git_data()
        if len(raw_node) > 0
    ]
    return [node for node in node_changes if node.filepath[:3] == root_dir]


def main():
    root_dir = "src"
    change_list = git_changes(root_dir)
    tree = FileTree(root_dir)
    for change in change_list:
        if change.type == "A":
            tree.add_file(change.filepath)
        if change.type == "M":
            tree.register_modification(change.filepath)
    tree.print()


if __name__ == "__main__":
    main()
