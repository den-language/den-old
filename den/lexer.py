from sly import Lexer

try:
    from helpers.utils import find_column
    import errors.errors as errors
    from helpers.location import Location
except ModuleNotFoundError:
    from den.helpers.utils import find_column
    import den.errors.errors as errors
    from den.helpers.location import Location


class DenLexer(Lexer):
    def set_logger(self, logger):
        self.logger = logger

    tokens = {INT, COLON, NEWLINE, ID, FAT_ARROW, RET, STRING}

    ignore = " \t"

    literals = {"{", "}", "(", ")", "=", ",", ":", "+", "-", "/", "*", "&", "%", ";"}

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
        self.logger.error(
            errors.unrecognized_character_error,
            f"Illegal character `{t.value[0]}`",
            Location(t.lineno, t.index),
        )
        self.index += 1
