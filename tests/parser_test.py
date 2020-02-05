from den.parser import DenParser
from den.lexer import DenLexer

def test_parser_1():
    lexer = DenLexer()
    parser = DenParser()
    text = """
int add() => {
    
}
"""
    result = parser.parse(lexer.tokenize(text))
    print(result)
    assert 0
