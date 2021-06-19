import dataclasses
import os
import re

TOKEN_TYPES = [
    [r"\bdef\b", "def"],
    [r"\bend\b", "end"],
    [r"\b[a-zA-Z]+\b", "identifier"],
    [r"\b[0-9]+\b", "integer"],
    [r"\(", "oparen"],
    [r"\)", "cparen"],
]


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
        tokens = []
        for x in self.file.read().split():
            tokens.extend(self._tokenize_one_token(x))
        return tokens

    def _tokenize_one_token(self, x):
        for token_type in TOKEN_TYPES:
            matching_token = f"\A{token_type[0]}"
            search_result = re.search(matching_token, x)
            if search_result:
                length = search_result.span()[1] - search_result.span()[0]
                if length != len(search_result.string):
                    remaining = search_result.string[length:]
                    result = [Token(token_type=token_type[1], value=x[0:length])]
                    result.extend(self._tokenize_one_token(remaining))
                    return result
                else:
                    return [Token(token_type=token_type[1], value=x)]
        raise CouldNotMatchTokenException(f"could not match {x} to any tokens")


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return ""


tokens = Tokenizer("test.js").tokenize()
print("".join([str(token) + "\n" for token in tokens]))

tree = Parser(tokens).parse()
print(tree)
