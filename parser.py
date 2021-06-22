from typing import List

from models import Token
from enums import TokenTypeEnum
from node_definitions import DefNode, VarRef, CallNode, IntegerNode


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
