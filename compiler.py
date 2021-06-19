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

    # def file_read(self):
    #     f = self.file
    #     current_string = f.read(1)
    #     while f.tell() != -1:
    #         print(current_string)
    #         current_string = f.read(1)

    def tokenize(self):
        tokens = []
        for x in self.file.read().split():
            tokens.append(self._tokenize_one_token(x))
        return tokens

    @staticmethod
    def _tokenize_one_token(x):
        for token_type in TOKEN_TYPES:

            matching_token = f"\A{token_type[0]}"
            print(matching_token)
            search_result = re.search(matching_token, x)
            print(search_result)
            if search_result:
                print(f"match! {x} {token_type}")
                return Token(token_type=token_type[1], value=x)
        raise CouldNotMatchTokenException(f"could not match {x} to any tokens")


class Parse:
    pass

tokens = Tokenizer("test.js").tokenize()
print("".join([str(token) + "\n" for token in tokens]))

tree = Parser(tokens).parse()
print(tree)
