from typing import List
from dataclasses import dataclass
import re

KEYWORDS = {'begin', 'end', 'gnd', 'voltagesource',
            'voltageprobe', 'currentsource', 
            'currentprobe', 'resistor', 
            'capacitor', 'inductor', 'diode', 'EOF'}
TOKEN_REG = [
    ('SCIENTIFIC', r'-?([1-9]\d*)(?:\.\d+)?(?:[eE][+\-]?\d+)'), 
    ('FLOAT', r'\d+(\.\d*)'),
    ('ID', r'[A-Za-z_]+[0-9]*'), 
    ('INT', r'[0-9]+'),
    ('EQ', r'='),
    ('NEXT_LINE', r'\n'),
    ('CONNECTOR', r'--'), 
    ('LP', r'\('), 
    ('RP', r'\)'), 
    ('LB', r'\['), 
    ('RB', r'\]'), 
    ('COMMA', r','), 
    ('SKIP', r'[ \t]')
]   

@dataclass
class Token:
    type: str
    value: str 
    line: int 
    column: int


class Scanner:
    def __init__(self, source_path: str) -> None:
        self.source_path = source_path
        self.source = self.load_source()
        self.clean_source = re.sub(r'(\#.+)', '', self.source)

        self.tokens = self.tokenize()

    def load_source(self) -> str:
        source = ""
        with open(self.source_path, 'r', encoding='utf-8') as source_file:
            source = source_file.read()

        return source

    def tokenize(self) -> List[Token]:
        tokens = []
        tok_regex = '|'.join('(?P<%s>%s)' % pair for pair in TOKEN_REG)
        get_token = re.compile(tok_regex).match
        line = 1
        current_position = line_start = 0
        match = get_token(self.clean_source)

        while match:
            type = match.lastgroup
            if type == 'NEXT_LINE':
                tokens.append(Token(type, '\n', line, match.start()-line_start))
                line_start = current_position
                line += 1
            elif type != 'SKIP':
                value = match.group(type)
                if type == 'ID' and value in KEYWORDS:
                    type = value
                tokens.append(Token(type, value, line, match.start()-line_start))
            current_position = match.end()
            match = get_token(self.clean_source, current_position)
        if current_position != len(self.clean_source):
            raise RuntimeError(f'Error while scanning source code file: \
                                Unexpected character {self.clean_source[current_position]} in line {line}')
        tokens.append(Token('EOF', '', line, current_position-line_start))
        return tokens
