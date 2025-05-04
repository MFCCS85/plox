import sys
from tokens import Token, TokenType


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
                self.had_error = False
            except EOFError:
                print()
                break

    def run(self, source: str) -> None:
        # Trying to solve the circular dependency I created in trying to follow the book as faithfully as possible...
        from scanner import Scanner

        scanner = Scanner(source, self)
        scanner.scan_tokens()

    def error(self, line: int, message: str) -> None:
        self.report(line, "", message)

    def report(self, line: int, where: str, message: str) -> None:
        print(f"[line {line}] Error {where}: {message}")
        self.had_error = True


if __name__ == "__main__":
    Plox(sys.argv)
