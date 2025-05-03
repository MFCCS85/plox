import sys
from enum import Enum, auto


class Plox:
    def __init__(self, argv: list[str]) -> None:
        self.had_error = False

        if len(argv) > 2:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(argv) == 2:
            self.run_file(argv[1])
        else:
            self.run_prompt()

    def run_file(self, path: str) -> None:
        src = ""
        with open(path, "r") as file:
            src = file.read()
        self.run(src)

    def run_prompt(self) -> None:
        while True:
            try:
                print(">> ", end="")
                line = input()
                if line.strip().lower() in ("exit", "quit"):
                    break
                self.run(line)
                self.had_error = True
            except EOFError:
                print()
                break

    def run(self, source: str) -> None:
        scanner = Scanner(source)
        scanner.scan_tokens()

    def error(self, line: int, message: str) -> None:
        self.__report(line, "", message)

    def __report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True


class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens: list[Token] = []
        self.start: int = 0
        self.current: int = 0
        self.line: int = 0

    def scan_tokens(self) -> list[Token]:
        while not is_at_end():
            start = current


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACE = auto()
    RIGHT_BRACE = auto()
    COMMA = auto()
    DOT = auto()
    MINUS = auto()
    PLUS = auto()
    SEMICOLON = auto()
    SLASH = auto()
    STAR = auto()

    # One or two character tokens.
    BANG = auto()
    BANG_EQUAL = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    GREATER = auto()
    GREATER_EQUAL = auto()
    LESS = auto()
    LESS_EQUAL = auto()

    # Literals.
    IDENTIFIER = auto()
    STRING = auto()
    NUMBER = auto()

    # Keywords.
    AND = auto()
    CLASS = auto()
    ELSE = auto()
    FALSE = auto()
    FUN = auto()
    FOR = auto()
    IF = auto()
    NIL = auto()
    OR = auto()
    PRINT = auto()
    RETURN = auto()
    SUPER = auto()
    THIS = auto()
    TRUE = auto()
    VAR = auto()
    WHILE = auto()

    EOF = auto()


class Token:
    def __init__(self, token_type: TokenType, lexeme: str, literal: object, line: int):
        self.token_type = token_type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line

    def to_string(self) -> str:
        return f"{self.token_type} {self.lexeme} {self.literal}"


if __name__ == "__main__":
    Plox(sys.argv)
