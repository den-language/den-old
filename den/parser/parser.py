from sly import Parser
from lexer import DenLexer
import ast

# TODO: Make this work
class DenParser:
    tokens = DenLexer.tokens


    # Meta grammar rules

    @_("block")
    def program(self, p):
        return ast.meta.Program(p)

    @_("block statement")
    def block(self, p):
        p.block.push(p.statement)
        return p.block

    @_("statement")
    def block(self, p):
        statement = ast.meta.Block([p])
        return statement

    @_("empty")
    def block(self, p):
        return ast.meta.Block([])
    

    # Statements

    @_("function_declaration")
    def statement(self, p):
        return 
    

    # Empty

    @_("")
    def empty(self, p):
        pass

