try:
    import parser.den_ast as ast
except:
    import den.parser.den_ast as ast

class CodeGen:
    def __init__(self, ast=None, debug=False):
        self.ast = ast
        self.debug = debug
        self.code = []

    def traverse(self, node):
        print(node)
        if isinstance(node, ast.meta.Program):
            self.code.append(node.dump())
    
    def generate(self, ast):
        self.ast = ast
        self.traverse(ast)
