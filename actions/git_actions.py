""" Git related Actions"""

import subprocess
from entities.git_change import GitChange
import logging


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


def __desserialized_git_changes(
    raw_git_data: list[str], root_dir: str = "src"
) -> list[GitChange]:
    """Method that get git changes"""
    node_changes = [
        GitChange.from_string(raw_node)
        for raw_node in raw_git_data
        if len(raw_node) > 0
    ]
    return [node for node in node_changes if node.filepath[:3] == root_dir]


def git_changes(repository_location: str, root_dir: str):
    """Get Git Changes from the repository"""
    try:
        raw_git_data = __raw_git_data(repository_location)
        return __desserialized_git_changes(raw_git_data, root_dir)
    except subprocess.CalledProcessError as error:
        logging.error(
            "%s: Error on execution of git command for the %s",
            error,
            repository_location,
        )
