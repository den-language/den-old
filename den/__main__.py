from parser import DenParser
from lexer import DenLexer
from codegen import CodeGen

lexer = DenLexer()
parser = DenParser()
text = """
int add() => {

}
"""
result = parser.parse(lexer.tokenize(text))
result.add_name("hello.den")
codegen = CodeGen()
codegen.generate(result)
