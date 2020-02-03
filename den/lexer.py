from sly import Lexer
from .utils import find_column

class DenLexer(Lexer):
    tokens = {
        INT,
        COLON,
        NEWLINE,
        ID,
        FAT_ARROW,
    }

    ignore = " \t"

    literals = { "{", "}", "(", ")", "=", ",", ":", "+", "-", "/", "*", "&", ";"}

    # Tokens
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    # ID["func"] = FUNC

    INT = r"\d+"
    FAT_ARROW = r"=>"
    
    ignore_comment = r"\#.*"
    # Extra action for newlines
    @_(r"\n+")
    def NEWLINE(self, t):
        self.lineno += t.value.count("\n")

    def error(self, t):
        print(f"Illegal character `{t.value[0]}` at line {self.lineno} col {find_column(self.text, t)}")
        self.index += 1

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
