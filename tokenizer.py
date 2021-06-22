import re

from models import Token
from enums import TOKEN_TYPES
from exceptions import CouldNotMatchTokenException


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
