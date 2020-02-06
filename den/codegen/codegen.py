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
        print(node)
        if isinstance(node, ast.meta.Program):
            self.builder.push("FRONT", node.dump())
        
    
    def generate(self, ast):
        self.ast = ast
        self.builder = Builder(self.ast.name)
        self.traverse(ast)
        print(self.builder.output())
