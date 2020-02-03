from sly import Parser
from lexer import DenLexer

# TODO: Make this work
class DenParser:
    tokens = DenLexer.tokens

    @_("block statement")
    def block(self, p):
        return p.program + (p.statement)

    @_("statement")
    def block(self, p):
        return (p.statement)

    @_("empty")
    def block(self, p):
        return ()
