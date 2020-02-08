from sly import Lexer

try:
    from utils import find_column
except ModuleNotFoundError:
    from den.utils import find_column


class DenLexer(Lexer):
    tokens = {INT, COLON, NEWLINE, ID, FAT_ARROW, RET, STRING}

    ignore = " \t"

    literals = {"{", "}", "(", ")", "=", ",", ":", "+", "-", "/", "*", "&", ";", "%"}

    # Tokens

    # String (yes that many backslashes for escape)
    STRING = r"(\".*?(?<!\\)(\\\\)*\"|'.*?(?<!\\)(\\\\)*')"

    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID["ret"] = RET

    INT = r"\d+"
    FAT_ARROW = r"=>"

    ignore_comment = r"\#.*"

    # Extra action for newlines
    @_(r"\n+")
    def NEWLINE(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print(
            f"Illegal character `{t.value[0]}` at line \
                {self.lineno} col {find_column(self.text, t.index)}"
        )
        self.index += 1
        raise SyntaxError
