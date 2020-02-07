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
            # TODO get error reporting working
            raise NameError(f"ERROR: redefinition of {funcname}")
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
        
        for statement in node.block.statements:
            self._codegen(statement)

        # retval = self._codegen()
        # self.builder.ret(retval)
        return func
    
    def _create_entry_block_alloca(self, name, _type):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        return builder.alloca(_type, size=None, name=name)

    def _codegen_VariableAssign(self, node):
        old_bindings = []

        if node.value is not None:
            init_val = self._codegen(node.value)
        else:
            pass # init_val = ir.Constant(ir.DoubleType(), 0.0)
        saved_block = self.builder.block
        var_addr = self._create_entry_block_alloca(node.id.name, init_val.type)
        self.builder.position_at_end(saved_block)
        self.builder.store(init_val, var_addr)

        old_bindings.append(self.func_symtab.get(node.id.name))
        self.func_symtab[node.id.name] = var_addr
    
    def _codegen_Return(self, node):
        retval = self._codegen(node.value)
        self.builder.ret(retval)

    def _codegen_Type(self, node):
        if node.name == "int":
            return ir.IntType(32)
        
    def _codegen_Integer(self, node):
        return ir.Constant(ir.IntType(32), int(node.value))
    
    def generate(self, _ast):
        assert isinstance(_ast, ast.meta.Program)
        self.ast = _ast
        self.module = ir.Module(name=self.ast.name)
        self.generate_code(self.ast)
        print(self.module)
