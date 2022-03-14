from typing import List


class Scanner:
    def __init__(self, source_path: str) -> None:
        self.source_path = source_path
        self.source = self.load_source()

    def load_source(self) -> str:
        source = ""
        with open(self.source_path, 'r', encoding='utf-8') as source_file:
            source = source_file.read()

        return source

    def tokenize(self) -> List:
        #TODO
        pass