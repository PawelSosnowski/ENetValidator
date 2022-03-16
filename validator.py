from scanner import Scanner, Token
from argparse import ArgumentParser
from typing import List


def parse_args():
    parser = ArgumentParser()
    parser.add_argument('--source_path', type=str, required=True, help='path to .net file with code.')

    arguments = parser.parse_args()

    return arguments


class Validator:
    def __init__(self, tokens: List) -> None:
        self.tokens = tokens
        self.iter = 0
        self.current_token  = lambda : self.tokens[self.iter]
        self.line_between = False

    def __error(self, message: str, token: Token= None):
        if token:
            raise RuntimeError(f'Parse error: {message}, in line: {token.line}, column: {token.column}')
        else:
            raise RuntimeError(f'Parse error: {message}')

    def validate(self) -> None:
        if self.current_token().type == 'begin':
            self.__commands()
            if self.current_token().type != 'end':
                self.__error('Unexpected token', self.current_token())
            self.iter += 1
            if self.current_token().type == 'NEXT_LINE':
                self.iter += 1
            if self.current_token().type != 'EOF':
                self.__error('Unexpected token', self.current_token())
            
    def __commands(self):
        self.iter += 1
        token = self.current_token()

        while token.type == 'NEXT_LINE':
            self.iter += 1
            token = self.current_token()

        if token.type == 'ID' or token.type == 'gnd':
            self.__command()
            self.__commands()

    def __command(self):
        token = self.current_token()
        
        if token.type == 'ID':
            self.iter += 1 
            token = self.current_token()
            if token.type == 'LB':
                self.__element_connections()
            elif token.type == 'EQ':
                self.__element_declaration()
            else:
                self.__error('Epsilon not allowed')
        elif token.type == 'gnd':
            self.iter += 1
            self.__element_connections()
        else:
            self.__error('Epsilon not allowed')

    def __element_declaration(self):
        if self.current_token().type == 'EQ':
            self.__net_element()
    
    def __element_connections(self):
        self.iter -= 1

        if not self.line_between:
            if self.tokens[self.iter-1].type != 'NEXT_LINE' or self.tokens[self.iter-2].type != 'NEXT_LINE':
                print(self.tokens[self.iter-1], self.tokens[self.iter-2])
                self.__error('There have to be new line between declaration and connection sections!')
            else:
                self.line_between = True

        if self.current_token().type == 'ID' or self.current_token().type == 'gnd':
            self.__vec_id()
            if self.current_token().type != 'CONNECTOR':
                self.__error('Unexpected token', self.current_token())
            else:
                self.iter += 1
                self.__vec_id()
                self.__element_connection()
        else:
            pass

    def __element_connection(self):
        if self.current_token().type == 'CONNECTOR':
            self.iter += 1
            self.__vec_id()
            self.__element_connection()
        elif self.current_token().type == 'NEXT_LINE':    
            self.iter += 1
            self.__element_connections()
        else:
            pass
        
    def __vec_id(self):
        if self.current_token().type == 'gnd':
            self.iter += 1
            return
        elif self.current_token().type == 'ID':
            self.iter += 1
            if self.current_token().type == 'LB':
                self.iter += 1
                if self.current_token().type == 'INT':
                    self.iter += 1
                    if self.current_token().type == 'RB':
                        self.iter += 1
                        return
        self.__error('Unexpected token', self.current_token())                

    def __net_element(self):
        self.iter += 1
        self.__type()
        self.iter += 1
        self.__parameters()
    
    def __type(self):
        if self.current_token().type in ['voltagesource',
            'voltageprobe', 'currentsource', 
            'currentprobe', 'resistor', 
            'capacitor', 'inductor', 'diode']:
            pass
        else:
            self.__error('Unexpected token', self.current_token())

    
    def __parameters(self):
        if self.current_token().type != 'LP':
            self.__error('Unexpected token', self.current_token())
        self.iter += 1
        self.__parameter()
        if self.current_token().type != 'RP':
            self.__error('Unexpected token', self.current_token())
        
        if self.current_token().type == 'NEXT_LINE':
            self.iter += 1

    def __parameter(self):
        if self.current_token().type in ['INT', 'FLOAT', 'SCIENTIFIC']:
            self.iter += 1
        elif self.current_token().type == 'ID':
            self.iter += 1
            if self.current_token().type == 'EQ':
                self.iter += 1
                if self.current_token().type in ['INT', 'FLOAT', 'SCIENTIFIC']:
                    self.iter += 1
                else:
                    self.__error('Unexpected token', self.current_token())
            else:
                self.__error('Unexpected token', self.current_token())
            
            self.__another_parameter()
        else:
            pass

    def __another_parameter(self):
        if self.current_token().type == 'COMMA':
            self.iter += 1
            if self.current_token().type == 'ID':
                self.iter += 1
                if self.current_token().type == 'EQ':
                    self.iter += 1
                    if self.current_token().type in ['INT', 'FLOAT', 'SCIENTIFIC']:
                        self.iter += 1
                        return
            else:
                self.__error('Unexpected token', self.current_token())
        else:
            pass


def main():
    args = parse_args()
    
    scanner = Scanner(args.source_path)
    print('Source file: \n\n', scanner.source)

    validator = Validator(scanner.tokens)
    validator.validate()
    print('STATUS: SUCCESS')

if __name__ == '__main__':
    main()
