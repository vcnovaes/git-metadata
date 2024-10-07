"""Git log object"""


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
