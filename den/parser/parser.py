from sly import Parser
from den.lexer import DenLexer
import den.parser.den_ast as ast
import den.helpers.location as location

# TODO: Make this work
class DenParser(Parser):
    tokens = DenLexer.tokens


    # Meta grammar rules

    @_("block")
    def program(self, p):
        return ast.meta.Program(p, p.block.position)

    @_("block statement")
    def block(self, p):
        p.block.push(p.statement)
        return p.block

    @_("statement")
    def block(self, p):
        statement = ast.meta.Block([p], p.statement[1].position)
        return statement

    @_("empty")
    def block(self, p):
        return ast.meta.Block([], 0)
    

    # Statements

    @_("function_definition")
    def statement(self, p):
        return p
    

    # Functions

    @_("type_id name_id '(' ')' FAT_ARROW '{' block '}'")
    def function_definition(self, p):
        return ast.functions.FunctionDefinition(
            p.type_id,
            p.name_id,
            ast.functions.Arguments(
                positional=ast.functions.PositionalArguments([]),
                keyword=ast.functions.KeywordArguments([])
            ),
            p.block,
            location.Location(p.type_id.position.sline, p.type_id.position.scol),
        )
    

    # Expressions

    @_("ID")
    def type_id(self, p):
        return ast.primitives.Type(p.ID, location.Location(p.lineno, p.index))

    @_("ID")
    def name_id(self, p):
        return ast.primitives.NameID(p.ID, location.Location(p.lineno, p.index))

    # Empty

    @_("")
    def empty(self, p):
        pass

