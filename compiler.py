import dataclasses
import re
from typing import List


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
        name = self.consume("identifier")
        return name

    def consume(self, expected_type):
        token = self.tokens.pop(0)
        if token.token_type == expected_type:
            return token

        raise RuntimeError(f"Expected token type {expected_type} but got {token.token_type}")


def main():
    tokens = Tokenizer("test.js").tokenize()

    print("".join([str(token) +
                   f"{NL if index < len(tokens) - 1 else ''}"
                   for index, token in enumerate(tokens)]
                  )
          )

    tree = Parser(tokens).parse()
    print(tree)


if __name__ == '__main__':
    main()
