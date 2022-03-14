from scanner import Scanner
from argparse import ArgumentParser
from typing import List


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--source_path', type=str, required=True, help='path to .net file with code.')

    arguments = parser.parse_args()

    return arguments


class Validator():
    def __init__(self, tokens: List) -> None:
        self.tokens = tokens

    def validate(self) -> None:
        #TODO
        pass


def main():
    args = parse_args()
    
    scanner = Scanner(args.source_path)
    print('Source file: \n\n', scanner.source)
    tokens = scanner.tokenize()
    
    validator = Validator(tokens)
    validator.validate()


if __name__ == '__main__':
    main()
