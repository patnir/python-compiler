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
class VarRef:
    value: str


@dataclasses.dataclass
class CallNode:
    name: str
    arg_expressions: Union[List[str], List[VarRef], List[int]]


@dataclasses.dataclass
class DefNode:
    name: str
    arg_names: List[str]
    body: Union[IntegerNode, CallNode, VarRef]

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
        self.consume("oparen")
        arg_names = self.parse_list(self.parse_identifier)
        self.consume("cparen")
        body = self.parse_expression()
        self.consume("end")
        return DefNode(name, arg_names, body)

    def parse_identifier(self):
        return self.consume("identifier").value

    def parse_var_ref(self):
        return VarRef(self.consume("identifier").value)

    def peek(self, token_type, offset=0):
        return self.tokens[offset].token_type == token_type

    def parse_expression(self):
        if self.peek("integer"):
            return self.parse_integer().value
        if self.peek("identifier") and self.peek("oparen", 1):
            return self.parse_call()
        # problem with this is that the body can be a variable
        return self.parse_var_ref()

    def parse_call(self):
        name = self.consume("identifier").value
        self.consume("oparen")
        arg_expressions = self.parse_list(self.parse_expression)
        self.consume("cparen")
        return CallNode(name, arg_expressions)

    def parse_list(self, parse_function):
        arg_list = []
        if not self.peek("cparen"):
            arg_list.append(parse_function())
            while self.peek("comma"):
                self.consume("comma")
                arg_list.append(parse_function())
        return arg_list

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
    compile_file("test2.js")
