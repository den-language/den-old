from sly import Parser

try:
    from lexer import DenLexer
    import parser.den_ast as ast
    import helpers.location as location
except ModuleNotFoundError:
    from den.lexer import DenLexer
    import den.parser.den_ast as ast
    import den.helpers.location as location


class DenParser(Parser):
    tokens = DenLexer.tokens
    debugfile = "parser.out"

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

    @_("variable_assign")
    def statement(self, p):
        return p.variable_assign

    @_("ret")
    def statement(self, p):
        return p.ret

    # Functions

    @_("type_id name_id '(' ')' FAT_ARROW '{' block '}'")
    def function_definition(self, p):
        p.block.label = "entry"
        return ast.functions.FunctionDefinition(
            p.type_id,
            p.name_id,
            ast.functions.Arguments(
                positional=ast.functions.PositionalArguments([]),
                keyword=ast.functions.KeywordArguments([]),
            ),
            p.block,
            location.Location(p.type_id.position.sline, p.type_id.position.scol),
        )

    @_("RET expr ';'")
    def ret(self, p):
        return ast.functions.Return(
            p.expr,
            location.Location(
                p.lineno,
                p.index,
                eline=p.expr.position.sline,
                ecol=p.expr.position.ecol,
            ),
        )

    # Variables

    @_("type_id ':' name_id '=' expr ';'")
    def variable_assign(self, p):
        return ast.variables.VariableAssign(
            p.type_id,
            p.name_id,
            p.expr,
            location.Location(
                p.type_id.position.sline,
                p.type_id.position.scol,
                eline=p.expr.position.sline,
                ecol=p.expr.position.ecol,
            ),
        )

    # Expressions

    @_("ref_id")
    def expr(self, p):
        return p.ref_id

    @_("integer")
    def expr(self, p):
        return p.integer

    @_("INT")
    def integer(self, p):
        return ast.primitives.Integer(p.INT, location.Location(p.lineno, p.index))

    # Maths with expressions

    @_("'-' expr %prec UMINUS")
    def expr(self, p):
        return ast.maths.Neg(
            p.expr, location.Location(p.expr.position.sline, p.expr.position.scol)
        )

    @_("expr '+' expr")
    def expr(self, p):
        return ast.maths.Add(
            p.expr0,
            p.expr1,
            location.Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '-' expr")
    def expr(self, p):
        return ast.maths.Sub(
            p.expr0,
            p.expr1,
            location.Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '/' expr")
    def expr(self, p):
        return ast.maths.Div(
            p.expr0,
            p.expr1,
            location.Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '*' expr")
    def expr(self, p):
        return ast.maths.Mul(
            p.expr0,
            p.expr1,
            location.Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("expr '%' expr")
    def expr(self, p):
        return ast.maths.Mod(
            p.expr0,
            p.expr1,
            location.Location(p.expr0.position.sline, p.expr0.position.scol),
        )

    @_("'(' expr ')'")
    def expr(self, p):
        return p.expr

    # IDs

    @_("ID")
    def type_id(self, p):
        return ast.primitives.Type(p.ID, location.Location(p.lineno, p.index))

    @_("ID")
    def name_id(self, p):
        return ast.primitives.NameID(p.ID, location.Location(p.lineno, p.index))

    @_("ID")
    def ref_id(self, p):
        return ast.primitives.RefID(p.ID, location.Location(p.lineno, p.index))

    # Empty

    @_("%prec EMPTY")
    def empty(self, p):
        pass
