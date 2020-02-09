try:
    from helpers.color import Color
    from helpers.utils import find_column
except ImportError:
    from den.helpers.color import Color
    from den.helpers.utils import find_column


class Error:
    def __init__(self, error_type, message, location):
        self.error_type = error_type
        self.message = message
        self.location = location


class Logger:
    def __init__(self, filename, contents, debug=False):
        self.file = filename
        self.contents = contents
        self.debug = debug
        self.errors = []
        self.indent = "  "

    def log(self, message):
        if self.debug:
            print(f"{Color.BLUE}Debug{Color.RESET}: {message}")

    def get_lines_string(self, location):
        lineno = location.sline  # Starts at line 1

        newline_split = self.contents.split("\n")

        start_line = lineno - 1 if lineno == 1 else lineno - 2
        end_line = lineno if lineno > len(newline_split) else lineno + 1

        final = ""

        length = max([len(str(num + 1)) for num in range(start_line, end_line + 1)])
        for i, line in zip(
            range(start_line, end_line + 1), newline_split[start_line:end_line]
        ):
            final += f"{self.indent*2}{i+1}{' '*(length-len(str(i+1)))} | {line}\n"

        return final

    def error(self, error_type, message, location):
        self.errors.append(Error(error_type, message, location))

    def throw(self):
        if self.errors:
            print(
                f"\n{Color.RED}{Color.UNDERLINE}{Color.BOLD}{len(self.errors)} {'Errors' if len(self.errors) > 1 else 'Error'} Found:{Color.RESET}"
            )
            for error in self.errors:
                print(
                    f"\n{self.indent}{Color.RED}{Color.UNDERLINE}{error.error_type.name}{Color.RESET}\n"
                )
                print(self.get_lines_string(error.location))
                print(f"{self.indent*2}{Color.RED}{error.message}{Color.RESET}")
                print(
                    f"{self.indent*2}{Color.BLUE}{self.file}:{error.location.sline}:{find_column(self.contents, error.location.scol)}{Color.RESET}\n"
                )
            quit()
