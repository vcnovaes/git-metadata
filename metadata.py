"""Module for run on terminal"""

import subprocess
import fire


class FileNode:
    """Data reprentation of a file"""

    def __init__(self, label: str, count: int = 0, children=None) -> None:
        if children is None:
            self.children = dict()

        self.label = label
        self.count = count

    def __str__(self) -> str:
        return f"{self.label}"

    def __repr__(self) -> str:
        return f"{self.label}.count:{self.count}"


class FileTree:
    """File Tree"""

    def __init__(self, root_node_name: str) -> None:
        self.root = FileNode(root_node_name)

    def print(self, node: FileNode = None, counter=0):
        """Print the file tree"""
        if node is None:
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
        """ "Add the file on the filetree"""
        # adicionar na arvore
        path_nodes = self.__find_or_create_path(filename)
        # somar count nos anteriores
        for node in path_nodes:
            node.count += 1

    def register_modification(self, filename: str):
        """register the modification of an existing file"""
        self.add_file(filename)

    def delete_file(self, filename: str):
        """Delete file from the tree"""
        path_nodes = self.__find_or_create_path(filename)
        file_node = path_nodes[-1]
        parents = path_nodes[:-1]
        to_remove = [file_node]
        for parent in reversed(parents):
            if len(parent.children) == 1:
                to_remove.append(parent)
                file_node = parent
            else:
                del parent.children[file_node.label]
                break
        for file in to_remove:
            del file


class GitChange:
    """Class for store git changes"""

    def __init__(self, modification_type: str, filepath: str) -> None:
        self.type = modification_type
        self.filepath = filepath

    @staticmethod
    def from_string(raw_modification_log: str):
        """Method that desserialize the gitlog change"""
        try:
            change_type, filename = raw_modification_log.split("\t", 1)
            return GitChange(change_type, filename)
        except ValueError as error:
            print(f"ValueError: {error} \t {raw_modification_log} was not processed")

    def __str__(self) -> str:
        return f"{self.type, self.filepath}"


def __raw_git_data(repository_location: str):
    return (
        subprocess.run(
            ["git", "log", "--name-status", "--pretty=format:"],
            stdout=subprocess.PIPE,
            check=True,
            cwd=repository_location,
        )
        .stdout.decode()
        .splitlines()
    )


def git_changes(repository_location: str, root_dir: str = "src"):
    """Method that get git changes"""
    node_changes = [
        GitChange.from_string(raw_node)
        for raw_node in __raw_git_data(repository_location)
        if len(raw_node) > 0
    ]
    return [node for node in node_changes if node.filepath[:3] == root_dir]


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
