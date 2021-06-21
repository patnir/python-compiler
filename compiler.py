import dataclasses
import re
from typing import List, Union


@dataclasses.dataclass()
class TokenType:
    re_expression: str
    type: str


TOKEN_TYPES = [
    TokenType(r"\bdef\b", "def"),
    TokenType(r"\bend\b", "end"),
    TokenType(r"\b[a-zA-Z]+\b", "identifier"),
    TokenType(r"\b[0-9]+\b", "integer"),
    TokenType(r"\(", "oparen"),
    TokenType(r"\)", "cparen"),
    TokenType(r",", "comma"),
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


@dataclasses.dataclass
class IntegerNode:
    value: int


@dataclasses.dataclass
class CallNode:
    name: str
    arg_expressions: List[str]


@dataclasses.dataclass
class DefNode:
    name: str
    arg_names: List[str]
    body: Union[IntegerNode, CallNode]

    def __init__(self, name, arg_names, body):
        self.name = name
        self.arg_names = arg_names
        self.body = body


class Parser:
    def __init__(self, tokens):
        self.tokens: List[Token] = tokens

    def parse(self):
        return self.parse_def()

    def parse_def(self):
        self.consume("def")
        name = self.consume("identifier").value
        arg_names = self.parse_arg_names()
        body = self.parse_expression()
        self.consume("end")
        return DefNode(name, arg_names, body)

    def parse_arg_names(self):
        self.consume("oparen")
        arg_names = []
        if self.peek("identifier"):
            arg_names.append(self.consume("identifier").value)
        while self.peek("comma"):
            self.consume("comma")
            arg_names.append(self.consume("identifier").value)
        self.consume("cparen")
        return arg_names

    def peek(self, token_type):
        return self.tokens[0].token_type == token_type

    def parse_expression(self):
        if self.peek("integer"):
            return self.parse_integer()
        return self.parse_call()

    def parse_call(self):
        name = self.consume("identifier").value
        self.consume("oparen")
        arg_expressions = []
        if self.peek("identifier"):
            arg_expressions.append(self.consume("identifier").value)
        elif self.peek("integer"):
            arg_expressions.append(self.consume("integer").value)
        while self.peek("comma"):
            self.consume("comma")
            if self.peek("identifier"):
                arg_expressions.append(self.consume("identifier").value)
            elif self.peek("integer"):
                arg_expressions.append(self.consume("integer").value)
        self.consume("cparen")
        return CallNode(name, arg_expressions)

    def parse_integer(self):
        return IntegerNode(int(self.consume("integer").value))

    def consume(self, expected_type):
        token = self.tokens.pop(0)
        if token.token_type == expected_type:
            return token

        raise RuntimeError(f"Expected token type {expected_type} but got {token.token_type}")


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


if __name__ == '__main__':
    compile_file("test.js")
    compile_file("test1.js")
