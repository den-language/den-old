try:
    import parser.den_ast as ast
except:
    import den.parser.den_ast as ast

from llvmlite import ir

class ModuleCodeGen:
    def __init__(self, ast=None, debug=False):
        self.ast = ast
        self.debug = debug
        self.module = None
        self.builder = None

        self.func_symtab = {}

    def generate_code(self, node):
        for statement in node.block.statements:
            self._codegen(statement)
    
    def _codegen(self, node):
        """Node visitor. Dispatches upon node type.
        For AST node of class Foo, calls self._codegen_Foo. Each visitor is
        expected to return a llvmlite.ir.Value.
        """
        method = '_codegen_' + node.__class__.__name__
        return getattr(self, method)(node)
    
    def _codegen_FunctionDefinition(self, node):
        self.func_symtab = {}

        funcname = node.name.name

        func_ty = ir.FunctionType(
            self._codegen(node.return_type), 
            [self._codegen(rty) for rty in node.arguments.positional_arguments.arguments]
        )

        if funcname in self.module.globals:
            existing_func = self.module[funcname]
            print(f"WARNING: redefinition of {funcname}")
            func = self.module.globals[funcname]
        else:
            func = ir.Function(self.module, func_ty, funcname)
        
        entry_block = func.append_basic_block('entry')
        self.builder = ir.IRBuilder(entry_block)

        for i, arg in enumerate(func.args):
            arg.name = node.arguments.positional_arguments.arguments[i]
            alloca = self.builder.alloca(self._codegen(node.arguments.positional_arguments.arguments[i]), name=arg.name)
            self.builder.store(arg, alloca)
            self.func_symtab[arg.name] = alloca

        # TODO: Get this working
        # retval = self._codegen()
        # self.builder.ret(retval)
        return func
    
    def _codegen_Type(self, node):
        if node.name == "int":
            return ir.IntType(32)

    
    def generate(self, _ast):
        assert isinstance(_ast, ast.meta.Program)
        self.ast = _ast
        self.module = ir.Module(name=self.ast.name)
        self.generate_code(self.ast)
        print(self.module)
