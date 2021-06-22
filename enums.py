import dataclasses
from enum import Enum


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
