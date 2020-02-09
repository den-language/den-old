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

    # def create_arrow(self, pos, prev):
    #    return " " * (len(self.indent*2) + prev + pos + 1) + "^\n"

    def get_lines_string(self, location):
        lineno = location.sline  # Starts at line 1

        newline_split = self.contents.split("\n")

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
                    f"{self.indent*2}{Color.BLUE}{self.file}:{error.location.sline}:{find_column(self.contents, error.location.scol)-1}{Color.RESET}\n"
                )
            quit()
