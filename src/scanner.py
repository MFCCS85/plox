from plox import Plox
from tokens import Token, TokenType


class Scanner:
    def __init__(self, source: str, plox: Plox):
        self.source = source
        self.plox = plox
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 0

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def add_token(self, token_type: TokenType, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
        if c == "(":
            self.add_token(TokenType.LEFT_PAREN)
        elif c == ")":
            self.add_token(TokenType.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TokenType.LEFT_BRACE)
        elif c == "}":
            self.add_token(TokenType.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TokenType.COMMA)
        elif c == ".":
            self.add_token(TokenType.DOT)
        elif c == "-":
            self.add_token(TokenType.MINUS)
        elif c == "+":
            self.add_token(TokenType.PLUS)
        elif c == ";":
            self.add_token(TokenType.SEMICOLON)
        elif c == "*":
            self.add_token(TokenType.STAR)
        else:
            self.plox.error(self.line, "Unexpected character.")

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c
