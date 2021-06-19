import dataclasses
import re

TOKEN_TYPES = [
    [r"\bdef\b", "def"],
    [r"\bend\b", "end"],
    [r"\b[a-zA-Z]+\b", "identifier"],
    [r"\b[0-9]+\b", "integer"],
    [r"\(", "oparen"],
    [r"\)", "cparen"],
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

    def _tokenize_one_token(self, token):
        for token_type in TOKEN_TYPES:
            matching_token = rf"\A{token_type[0]}"
            search_result = re.search(matching_token, token)
            if search_result:
                length = search_result.span()[1] - search_result.span()[0]
                if length != len(search_result.string):
                    remaining = search_result.string[length:]
                    result = [Token(token_type=token_type[1], value=token[0:length])]
                    result.extend(self._tokenize_one_token(remaining))
                    return result
                return [Token(token_type=token_type[1], value=token)]
        raise CouldNotMatchTokenException(f"could not match {token} to any tokens")


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return ""


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
