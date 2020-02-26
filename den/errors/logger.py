import os

try:
    from helpers.color import Color
    from helpers.utils import find_column
except ImportError:
    from den.helpers.color import Color
    from den.helpers.utils import find_column


class Error:
    def __init__(self, error_type, message, location, file, other, tip):
        self.error_type = error_type
        self.message = message
        self.location = location
        self.file = file
        self.other = other
        self.tip = tip


class Logger:
    def __init__(self, filename, contents, debug=False):
        self.files = {os.path.abspath(filename): contents[1:]}
        self.debug = debug
        self.errors = []
        self.indent = "  "

    def log(self, message):
        if self.debug:
            print(f"{Color.BLUE}Debug{Color.RESET}: {message}\n")

    def status(self, message):
        if not self.debug:
            print(f"{message}")

    # def create_arrow(self, pos, prev):
    #    return " " * (len(self.indent*2) + prev + pos + 1) + "^\n"

    def get_lines_string(self, location, file):
        contents = self.files[os.path.abspath(file)]

        lineno = location.sline  # Starts at line 1

        newline_split = contents.split("\n")

        start_line = lineno - 1 if lineno == 1 else lineno - 2
        end_line = lineno if lineno > len(newline_split) else lineno + 1

        final = ""

        length = max([len(str(num + 1)) for num in range(start_line, end_line + 1)])
        remove_whitespace = (
            len(
                set(
                    [
                        len(line) - len(line.lstrip())
                        for line in newline_split[start_line:end_line]
                    ]
                )
            )
            <= 1
        )

        for i, line in zip(
            range(start_line, end_line + 1), newline_split[start_line:end_line]
        ):
            final += f"{self.indent*2}{i+1}{' '*(length-len(str(i+1)))} | {line if not remove_whitespace else line.lstrip()}\n"
            # if i == lineno-1:
            #    final += self.create_arrow(find_column(self.contents, location.scol), length)

        return final

    def error(self, error_type, message, location, other=[], filename=None, tip=None):
        if filename is None:
            filename = next(iter(self.files.keys()))
        self.errors.append(Error(error_type, message, location, filename, other, tip))
        for extra in other:
            if extra[1] not in self.files:
                with open(extra[1], "r") as f:
                    self.files[extra[1]] = f.read()

    def throw(self):
        if self.errors:
            print(
                f"\n{Color.RED}{Color.UNDERLINE}{Color.BOLD}{len(self.errors)} {'Errors' if len(self.errors) > 1 else 'Error'} Found:{Color.RESET}"
            )
            for error in self.errors:
                if not error.other:
                    print(
                        f"\n{self.indent}{Color.RED}{Color.UNDERLINE}{error.error_type.name}{Color.RESET}\n"
                    )
                    print(self.get_lines_string(error.location, error.file))
                    print(f"{self.indent*2}{Color.RED}{error.message}{Color.RESET}")
                    print(
                        f"{self.indent*2}{Color.BLUE}{os.path.relpath(error.file)}:{error.location.sline}:{find_column(self.files[error.file], error.location.scol)-1}{Color.RESET}\n"
                    )
                    if error.tip:
                        print(
                            f"{self.indent*2}{Color.GREEN}Tip: {error.tip}{Color.RESET}"
                        )
                else:
                    print(
                        f"\n{self.indent}{Color.RED}{Color.UNDERLINE}{error.error_type.name}{Color.RESET}\n"
                    )
                    print(self.get_lines_string(error.location, error.file))
                    print(f"{self.indent*2}{Color.RED}{error.message}{Color.RESET}")
                    print(
                        f"{self.indent*2}{Color.BLUE}{os.path.relpath(error.file)}:{error.location.sline}:{find_column(self.files[error.file], error.location.scol)-1}{Color.RESET}\n"
                    )
                    for other in error.other:
                        # other = [position, file, message]
                        print(self.get_lines_string(other[0], other[1]))
                        print(f"{self.indent*2}{Color.RED}{other[2]}{Color.RESET}")
                        print(
                            f"{self.indent*2}{Color.BLUE}{os.path.relpath(other[1])}:{other[0].sline}:{find_column(self.files[other[1]], other[0].scol)-1}{Color.RESET}\n"
                        )
                    if error.tip:
                        print(
                            f"{self.indent*2}{Color.GREEN}Tip: {error.tip}{Color.RESET}\n"
                        )

            quit(1)
