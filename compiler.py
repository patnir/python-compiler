import dataclasses
import re
import os
from enum import Enum
from typing import List

from node_definitions import DefNode, VarRef, CallNode, IntegerNode


class TokenTypeEnum(str, Enum):
    DEF = "def"
    END = "end"
    IDENTIFIER = "identifier"
    INTEGER = "integer"
    OPAREN = "oparen"
    CPAREN = "cparen"
    COMMA = "comma"


@dataclasses.dataclass()
class TokenType:
    re_expression: str
    type: str


TOKEN_TYPES = [
    TokenType(r"\bdef\b", TokenTypeEnum.DEF),
    TokenType(r"\bend\b", TokenTypeEnum.END),
    TokenType(r"\b[a-zA-Z]+\b", TokenTypeEnum.IDENTIFIER),
    TokenType(r"\b[0-9]+\b", TokenTypeEnum.INTEGER),
    TokenType(r"\(", TokenTypeEnum.OPAREN),
    TokenType(r"\)", TokenTypeEnum.CPAREN),
    TokenType(r",", TokenTypeEnum.COMMA),
]

NL = '\n'


@dataclasses.dataclass
class Token:
    token_type: str
    value: str


class CouldNotMatchTokenException(Exception):
    pass


class Tokenizer:

    def __init__(self, file_path):
        self.file = open(file_path, "r")

    def tokenize(self):
        result = []
        for token in self.file.read().split():
            result.extend(self._tokenize_one_token(token))
        return result

    @staticmethod
    def _get_search_result_length(search_result):
        return search_result.span()[1] - search_result.span()[0]

    def _tokenize_one_token(self, token):
        for token_type in TOKEN_TYPES:
            matching_token = rf"\A{token_type.re_expression}"
            search_result = re.search(matching_token, token)
            if search_result:
                length = self._get_search_result_length(search_result)
                if length != len(search_result.string):
                    remaining = search_result.string[length:]
                    result = [Token(token_type=token_type.type, value=token[0:length])]
                    result.extend(self._tokenize_one_token(remaining))
                    return result
                return [Token(token_type=token_type.type, value=token)]
        raise CouldNotMatchTokenException(f"could not match {token} to any tokens")


class Parser:
    def __init__(self, tokens):
        self.tokens: List[Token] = tokens

    def parse(self):
        return self.parse_def()

    def parse_def(self):
        self.consume(TokenTypeEnum.DEF)
        name = self.consume(TokenTypeEnum.IDENTIFIER).value
        self.consume(TokenTypeEnum.OPAREN)
        arg_names = self.parse_comma_separated_list(self.parse_identifier)
        self.consume(TokenTypeEnum.CPAREN)
        body = self.parse_expression()
        self.consume(TokenTypeEnum.END)
        return DefNode(name, arg_names, body)

    def parse_identifier(self):
        return self.consume(TokenTypeEnum.IDENTIFIER).value

    def parse_var_ref(self):
        return VarRef(self.consume(TokenTypeEnum.IDENTIFIER).value)

    def peek(self, token_type, offset=0):
        return self.tokens[offset].token_type == token_type

    def parse_expression(self):
        if self.peek(TokenTypeEnum.INTEGER):
            return self.parse_integer().value
        if self.peek(TokenTypeEnum.IDENTIFIER) and self.peek(TokenTypeEnum.OPAREN, 1):
            return self.parse_call()
        # problem with this is that the body can be a variable
        return self.parse_var_ref()

    def parse_call(self):
        name = self.consume(TokenTypeEnum.IDENTIFIER).value
        self.consume(TokenTypeEnum.OPAREN)
        arg_expressions = self.parse_comma_separated_list(self.parse_expression)
        self.consume(TokenTypeEnum.CPAREN)
        return CallNode(name, arg_expressions)

    def parse_comma_separated_list(self, parse_function, end_identifier=TokenTypeEnum.CPAREN):
        """
        end_identifier: this could be ")", "]", etc.
        """
        arg_list = []
        if not self.peek(end_identifier):
            arg_list.append(parse_function())
            while self.peek(TokenTypeEnum.COMMA):
                self.consume(TokenTypeEnum.COMMA)
                arg_list.append(parse_function())
        return arg_list

    def parse_integer(self):
        return IntegerNode(int(self.consume(TokenTypeEnum.INTEGER).value))

    def consume(self, expected_type):
        token = self.tokens.pop(0)
        if token.token_type == expected_type:
            return token

        raise RuntimeError(f"Expected token type {expected_type} but got {token.token_type}")


class Generator:
    def __init__(self):
        pass

    def generate(self, node):
        if isinstance(node, DefNode):
            return f"def {node.name}({','.join(node.arg_names)}): return {node.body}"
        raise RuntimeError(f"Unexpected ndoe type: {type(node)}")


class WriteCodeToFile:
    def __init__(self, code):
        self.code = code

    def write_to_working_directory(self, file_path):
        with open(os.getcwd() + f"/outputs/{file_path}", "w") as file:
            file.write(self.code)


def compile_file(file_name):
    tokens = Tokenizer(file_name).tokenize()
    print("===============")
    print("".join([str(token) +
                   f"{NL if index < len(tokens) - 1 else ''}"
                   for index, token in enumerate(tokens)]
                  )
          )

    tree = Parser(tokens).parse()
    print(tree)
    generated_code = Generator().generate(tree)
    print("++++++++++++")
    print(generated_code)
    WriteCodeToFile(generated_code).write_to_working_directory("result.py")


if __name__ == '__main__':
    compile_file("test3.js")
    # compile_file("test.js")
    # compile_file("test1.js")
    # compile_file("test2.js")
