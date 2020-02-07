from sly import Lexer
try:
    from utils import find_column
except ModuleNotFoundError:
    from den.utils import find_column

class DenLexer(Lexer):
    tokens = {
        INT,
        COLON,
        NEWLINE,
        ID,
        FAT_ARROW,
        RET,
        STRING
    }

    ignore = " \t"

    literals = { "{", "}", "(", ")", "=", ",", ":", "+", "-", "/", "*", "&", ";", "%"}

    # Tokens'
    STRING = r"(\".*?(?<!\\)(\\\\)*\"|'.*?(?<!\\)(\\\\)*')"  # String (yes that many backslashes for escape)

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
        print(f"Illegal character `{t.value[0]}` at line {self.lineno} col {find_column(self.text, t.index)}")
        self.index += 1
        raise SyntaxError

if __name__ == "__main__":
    file = """entry => {  # no arguments so we can skip the parenthesis
    int: x;
    int: y = &x - 1;  # Create a relationship between x and y

    x = 10;
    # Now y is 9

    x = 1203;
    # Now y is 1202
}"""
    lexer = DenLexer()
    for token in lexer.tokenize(file):
        print(token)
