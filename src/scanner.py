from plox import Plox
from tokens import Token, TokenType as TT


class Scanner:
    def __init__(self, source: str, plox: Plox):
        self.source = source
        self.plox = plox
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 0

        self.keywords = {
            "and": TT.AND,
            "class": TT.CLASS,
            "else": TT.ELSE,
            "false": TT.FALSE,
            "for": TT.FOR,
            "fun": TT.FUN,
            "if": TT.IF,
            "nil": TT.NIL,
            "or": TT.OR,
            "print": TT.PRINT,
            "return": TT.RETURN,
            "super": TT.SUPER,
            "this": TT.THIS,
            "true": TT.TRUE,
            "var": TT.VAR,
            "while": TT.WHILE,
        }

    def scan_tokens(self) -> list[Token]:
        while not self.is_at_end():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TT.EOF, "", None, self.line))
        return self.tokens

    def is_at_end(self) -> bool:
        return self.current >= len(self.source)

    def add_token(self, token_type: TT, literal: object = None):
        text = self.source[self.start : self.current]
        self.tokens.append(Token(token_type, text, literal, self.line))

    def scan_token(self):
        c = self.advance()
        # Single character
        if c == "(":
            self.add_token(TT.LEFT_PAREN)
        elif c == ")":
            self.add_token(TT.RIGHT_PAREN)
        elif c == "{":
            self.add_token(TT.LEFT_BRACE)
        elif c == "}":
            self.add_token(TT.RIGHT_BRACE)
        elif c == ",":
            self.add_token(TT.COMMA)
        elif c == ".":
            self.add_token(TT.DOT)
        elif c == "-":
            self.add_token(TT.MINUS)
        elif c == "+":
            self.add_token(TT.PLUS)
        elif c == ";":
            self.add_token(TT.SEMICOLON)
        elif c == "*":
            self.add_token(TT.STAR)

        # One or two characters
        elif c == "!":
            self.add_token(
                TT.BANG_EQUAL if self.match("=") else TT.BANG,
            )
        elif c == "=":
            self.add_token(
                TT.EQUAL_EQUAL if self.match("=") else TT.EQUAL,
            )
        elif c == "<":
            self.add_token(
                TT.LESS_EQUAL if self.match("=") else TT.LESS,
            )
        elif c == ">":
            self.add_token(
                TT.GREATER_EQUAL if self.match("=") else TT.GREATER,
            )

        # Literals
        elif c == '"':
            self.string()
        elif self.is_digit(c):
            self.number()

        # Keywords and Identifiers
        elif self.is_alpha(c):
            self.identifier()

        # Comments and whitespace
        elif c == "/":
            if self.match("/"):
                while self.peek() != "\n" and not self.is_at_end():
                    self.advance()
            else:
                self.add_token(TT.SLASH)
        elif c in " \r \t":
            pass
        elif c == "\n":
            self.line += 1

        else:
            self.plox.error(
                self.line,
                f"Unexpected character.",
            )

    def advance(self) -> str:
        c = self.source[self.current]
        self.current += 1
        return c

    def match(self, expected: str) -> bool:
        if self.is_at_end():
            return False
        if self.source[self.current] != expected:
            return False

        self.current += 1
        return True

    def peek(self) -> str:
        if self.is_at_end():
            return "\0"
        return self.source[self.current]

    def string(self) -> None:
        while self.peek() != '"' and self.is_at_end():
            if self.peek() == "\n":
                self.line += 1
            self.advance()

        if self.is_at_end():
            self.plox.error(self.line, "Unterminated string.")
            return

        self.advance()

        value = self.source[self.start + 1 : self.current - 1]
        self.add_token(TT.STRING, value)

    def number(self) -> None:
        while self.is_digit(self.peek()):
            self.advance()

        if self.peek() == "." and self.is_digit(self.peek_next()):
            self.advance()
            while self.is_digit(self.peek()):
                self.advance()

        self.add_token(TT.NUMBER, float(self.source[self.start : self.current]))

    def is_digit(self, char: str) -> bool:
        return ord(char) >= ord("0") and ord(char) <= ord("9")

    def peek_next(self) -> str:
        if self.current + 1 >= len(self.source):
            return "\0"
        return self.source[self.current + 1]

    def identifier(self) -> None:
        while self.is_alpha_numeric(self.peek()):
            self.advance()

        text = self.source[self.start : self.current]
        token_type = self.keywords.get(text, TT.IDENTIFIER)

        self.add_token(token_type)

    def is_alpha(self, char: str) -> bool:
        _char = ord(char)
        return (
            (_char >= ord("a") and _char <= ord("z"))
            or (_char >= ord("A") and _char <= ord("Z"))
            or (_char == ord("_"))
        )

    def is_alpha_numeric(self, char: str) -> bool:
        return self.is_alpha(char) or self.is_digit(char)
