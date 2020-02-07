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
    assert result.block.statements[0].return_type.name == "int"
    assert result.block.statements[0].name.name == "add"

def test_parser_2():
    lexer = DenLexer()
    parser = DenParser()
    text = """
int add() => {
    int: x = -10+10*10-(20%213)-10/10;
    int: y = x;
}
"""
    result = parser.parse(lexer.tokenize(text))
    assert result.block.statements[0].return_type.name == "int"
    assert result.block.statements[0].name.name == "add"
