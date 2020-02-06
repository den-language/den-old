try:
    import parser.den_ast as ast
except:
    import den.parser.den_ast as ast

from .builder import Builder

class CodeGen:
    def __init__(self, ast=None, debug=False):
        self.ast = ast
        self.debug = debug
        self.builder = None

    def traverse(self, node):
        if isinstance(node, ast.meta.Program):
            self.builder.push("FRONT", node.dump())
            self.traverse(node.block)
        
        elif isinstance(node, ast.meta.Block):
            for statement in node.statements:
                self.traverse(statement)
        
        elif isinstance(node, ast.functions.FunctionDefinition):
            self.builder.push("FUNCTIONS", node.dump())
    
    def generate(self, ast):
        self.ast = ast
        self.builder = Builder(self.ast.name)
        self.traverse(ast)
        print(self.builder.output())
