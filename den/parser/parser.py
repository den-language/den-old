from sly import Parser
import logging

try:
    from lexer import DenLexer
    import parser.den_ast as ast
    from helpers.location import Location
except ModuleNotFoundError:
    from den.lexer import DenLexer
    import den.parser.den_ast as ast
    from den.helpers.location import Location


# Arguments Constructor
def arguments_const(arguments: list):
    return ast.functions.Arguments(
        positional=ast.functions.PositionalArguments(arguments),
        keyword=ast.functions.KeywordArguments([]),
    )


class DenParser(Parser):
    tokens = DenLexer.tokens
    log = logging.getLogger()
    log.setLevel(logging.ERROR)
    # debugfile = "parser.out"

    precedence = (
        ("left", EMPTY),
        ("left", "+", "-"),
        ("left", "*", "/", "%"),
        ("right", UMINUS),
    )

    # Meta grammar rules

    @_("block")
    def program(self, p):
        return ast.meta.Program(p.block, p.block.position)

    @_("block statement")
    def block(self, p):
        p.block.push(p.statement)
        return p.block

    @_("statement")
    def block(self, p):
        statement = ast.meta.Block([p.statement], p.statement.position)
        return statement

    @_("empty")
    def block(self, p):
        return ast.meta.Block([], 0)

    # Statements

    @_("function_definition")
    def statement(self, p):
        return p.function_definition

    @_("variable_assign_full")
    def statement(self, p):
        return p.variable_assign_full

    @_("variable_dec")
    def statement(self, p):
        return p.variable_dec

    @_("variable_assign")
    def statement(self, p):
        return p.variable_assign

    @_("function_call ';'")
    def statement(self, p):
        return p.function_call

    @_("ret")
    def statement(self, p):
        return p.ret

    # Functions

    @_(
        "type_id name_id '(' id_items ')' FAT_ARROW '{' block '}'",
        "type_id name_id '(' id_items ',' ')' FAT_ARROW '{' block '}'",
    )
    def function_definition(self, p):
        p.block.label = "entry"
        return ast.functions.FunctionDefinition(
            p.type_id,
            p.name_id,
            arguments_const(p.id_items),
            p.block,
            Location(p.type_id.position.sline, p.type_id.position.scol),
        )

    @_(
        "type_id name_id '(' type_id ':' name_id ')' FAT_ARROW '{' block '}'",
        "type_id name_id '(' type_id ':' name_id ',' ')' FAT_ARROW '{' block '}'",
    )
    def function_definition(self, p):
        p.block.label = "entry"
        p.name_id1.type = p.type_id1
        return ast.functions.FunctionDefinition(
            p.type_id0,
            p.name_id0,
            arguments_const([p.name_id1]),
            p.block,
            Location(p.type_id0.position.sline, p.type_id0.position.scol),
        )

    @_(
        "type_id name_id '(' ')' FAT_ARROW '{' block '}'",
        "type_id name_id '(' ',' ')' FAT_ARROW '{' block '}'",
    )
    def function_definition(self, p):
        p.block.label = "entry"
        return ast.functions.FunctionDefinition(
            p.type_id,
            p.name_id,
            arguments_const([]),
            p.block,
            Location(p.type_id.position.sline, p.type_id.position.scol),
        )

    @_("name_id '(' ')'", "name_id '(' ',' ')'")
    def function_call(self, p):
        return ast.functions.FunctionCall(
            p.name_id,
            arguments_const([]),
            Location(p.name_id.position.sline, p.name_id.position.scol),
        )

    @_("name_id '(' expr ')'", "name_id '(' expr ',' ')'")
    def function_call(self, p):
        return ast.functions.FunctionCall(
            p.name_id,
            arguments_const([p.expr]),
            Location(p.name_id.position.sline, p.name_id.position.scol),
        )

    @_("name_id '(' items ')'", "name_id '(' items ',' ')'")
    def function_call(self, p):
        return ast.functions.FunctionCall(
            p.name_id,
            arguments_const(p.items),
            Location(p.name_id.position.sline, p.name_id.position.scol),
        )

    @_("RET expr ';'")
    def ret(self, p):
        return ast.functions.Return(
            p.expr,
            Location(
                p.lineno,
                p.index,
                eline=p.expr.position.sline,
                ecol=p.expr.position.ecol,
            ),
        )

    # Variables

    @_("type_id ':' name_id '=' expr ';'")
    def variable_assign_full(self, p):
        return ast.variables.VariableAssignFull(
            p.type_id,
            p.name_id,
            p.expr,
            Location(
                p.type_id.position.sline,
                p.type_id.position.scol,
                eline=p.expr.position.sline,
                ecol=p.expr.position.ecol,
            ),
        )

    @_("name_id '=' expr ';'")
    def variable_assign(self, p):
        return ast.variables.VariableAssign(
            p.name_id,
            p.expr,
            Location(
                p.name_id.position.sline,
                p.name_id.position.scol,
                eline=p.expr.position.sline,
                ecol=p.expr.position.ecol,
            ),
        )

    @_("type_id ':' name_id ';'")
    def variable_dec(self, p):
        return ast.variables.VariableDec(
            p.name_id,
            p.type_id,
            Location(
                p.type_id.position.sline,
                p.type_id.position.scol,
                eline=p.name_id.position.sline,
                ecol=p.name_id.position.ecol,
            ),
        )

    # Expressions

    @_("ref_id")
    def expr(self, p):
        return p.ref_id

    @_("integer")
    def expr(self, p):
        return p.integer

    @_("function_call")
    def expr(self, p):
        return p.function_call

    # Sub expressions

    @_("INT")
    def integer(self, p):
        return ast.primitives.Integer(p.INT, Location(p.lineno, p.index))

    @_("expr ',' expr")
    def items(self, p):
        return [p.expr0, p.expr1]

    @_("items ',' expr")
    def items(self, p):
        return [p.items] + [p.expr0]

    @_("type_id ':' name_id ',' type_id ':' name_id")
    def id_items(self, p):
        p.name_id0.type = p.type_id0
        p.name_id1.type = p.type_id1
        return [p.name_id0, p.name_id1]

    @_("id_items ',' type_id ':' name_id")
    def id_items(self, p):
        p.name_id.type = p.type_id
        return [p.id_items] + [p.name_id]

    # Maths with expressions

    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        return ast.maths.Neg(
            p.expr, Location(p.expr.position.sline, p.expr.position.scol)
        )

    @_("expr '+' expr")
    def expr(self, p):
        return ast.maths.Add(
            p.expr0, p.expr1, Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '-' expr")
    def expr(self, p):
        return ast.maths.Sub(
            p.expr0, p.expr1, Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '/' expr")
    def expr(self, p):
        return ast.maths.Div(
            p.expr0, p.expr1, Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '*' expr")
    def expr(self, p):
        return ast.maths.Mul(
            p.expr0, p.expr1, Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '%' expr")
    def expr(self, p):
        return ast.maths.Mod(
            p.expr0, p.expr1, Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    # IDs

    @_("ID")
    def type_id(self, p):
        return ast.primitives.Type(p.ID, Location(p.lineno, p.index))

    @_("ID")
    def name_id(self, p):
        return ast.primitives.NameID(p.ID, Location(p.lineno, p.index))

    @_("ID")
    def ref_id(self, p):
        return ast.primitives.RefID(p.ID, Location(p.lineno, p.index))

    # Empty

    @_("%prec EMPTY")
    def empty(self, p):
        pass
