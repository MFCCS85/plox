import sys


class Plox:
    def __init__(self, argv):
        if len(argv) > 1:
            print("Usage: jlox [script]")
            sys.exit(64)
        elif len(argv) == 1:
            self.run_file(argv[0])
        else:
            self.run_prompt()

    def run_file(self, path):
        print(path)

    def run_prompt(self):
        print("hii")


Plox(sys.argv)
