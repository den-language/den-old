from llvmlite import ir


class ModuleCodeGen:
    def __init__(self, _ast=None, debug=False):
        self.ast = _ast
        self.debug = debug
        self.module = None
        self.builder = None

        self.result = None

        self.builtin_types = {}

        self.symtab = {}

        self.functions = []

    def generate_code(self, node):
        for statement in node.block.statements:
            if statement.__class__.__name__ == "FunctionDefinition":
                addr = self._codegen_function_scaff(statement)
                self.functions.append((statement, addr))
            else:
                self._codegen(statement)
        for statement, addr in self.functions:
            self._codegen_FunctionDefinition(statement, addr)

    def _codegen(self, node):
        """Node visitor. Dispatches upon node type.
        For AST node of class Foo, calls self._codegen_Foo. Each visitor is
        expected to return a llvmlite.ir.Value.
        """
        method = "_codegen_" + node.__class__.__name__
        if node.__class__.__name__ in ["Add", "Sub", "Mul", "Div", "Mod"]:
            return self._codegen_BinaryOp(node)
        return getattr(self, method)(node)

    # Expressions

    def _codegen_Neg(self, node):
        return self.builder.neg(self._codegen(node.value), name="tmpneg")

    def _codegen_RefID(self, node):
        # TODO: Do error reporting
        variable = self.symtab[node.name]
        return self.builder.load(variable, node.name)

    def _codegen_BinaryOp(self, node):
        left = self._codegen(node.left)
        right = self._codegen(node.right)

        self.builtin_types = {  # skipcq
            "i32": {
                "Add": self.builder.add,
                "Sub": self.builder.sub,
                "Mul": self.builder.mul,
                "Div": self.builder.sdiv,
                "Mod": self.builder.srem,
            },
            "float": {
                "Add": self.builder.fadd,
                "Sub": self.builder.fsub,
                "Mul": self.builder.fmul,
                "Div": self.builder.fdiv,
                "Mod": self.builder.frem,
            },
        }

        node_name = node.__class__.__name__

        if str(left.type) != str(right.type):
            raise TypeError("error")  # TODO: Do error reporting
        elif (
            str(left.type) in self.builtin_types
            and node_name in self.builtin_types[str(left.type)]
        ):
            return self.builtin_types[str(left.type)][node_name](
                left, right, f"temp{str(left.type).lower()}"
            )
        else:
            raise NotImplementedError("error")  # TODO: Do error reporting

    # Functions

    def _create_entry_block_alloca(self, name, _type):
        """Create an alloca in the entry BB of the current function."""
        builder = ir.IRBuilder()
        builder.position_at_start(self.builder.function.entry_basic_block)
        return builder.alloca(_type, size=None, name=name)

    def _codegen_function_scaff(self, node):
        funcname = node.name.name
        func_ty = ir.FunctionType(
            self._codegen(node.return_type),
            [
                self._codegen(rty.type)
                for rty in node.arguments.positional_arguments.arguments
            ],
        )

        if funcname in self.module.globals:
            # TODO get error reporting working
            raise NameError(f"ERROR: redefinition of {funcname}")
        else:
            func = ir.Function(self.module, func_ty, funcname)

        return func

    def _codegen_FunctionDefinition(self, node, func):
        self.symtab = {}

        entry_block = func.append_basic_block("entry")
        self.builder = ir.IRBuilder(entry_block)

        for i, arg in enumerate(func.args):
            arg.name = node.arguments.positional_arguments.arguments[i].name
            alloca = self.builder.alloca(
                self._codegen(node.arguments.positional_arguments.arguments[i].type),
                name=arg.name,
            )
            self.builder.store(arg, alloca)
            self.symtab[arg.name] = alloca

        for statement in node.block.statements:
            self._codegen(statement)

        return func

    def _codegen_FunctionCall(self, node):
        # TODO: Error reporting
        called_function = self.module.get_global(node.name.name)
        # check if function
        call_args = [
            self._codegen(argument)
            for argument in node.arguments.positional_arguments.arguments
        ]
        return self.builder.call(called_function, call_args, "calltmp")

    def _codegen_Return(self, node):
        retval = self._codegen(node.value)
        self.builder.ret(retval)

    # Variables

    def _codegen_VariableAssignFull(self, node):
        init_val = self._codegen(node.value)
        saved_block = self.builder.block
        var_addr = self._create_entry_block_alloca(node.id.name, init_val.type)
        self.builder.position_at_end(saved_block)
        self.builder.store(init_val, var_addr)

        self.symtab[node.id.name] = var_addr

    def _codegen_VariableDec(self, node):
        var_type = self._codegen(node.type)
        var_addr = self._create_entry_block_alloca(node.id.name, var_type)
        self.symtab[node.id.name] = var_addr

    def _codegen_VariableAssign(self, node):
        init_val = self._codegen(node.value)
        saved_block = self.builder.block

        var_addr = self.symtab[node.id.name]  # TODO: Raise error if not initialized

        self.builder.position_at_end(saved_block)
        self.builder.store(init_val, var_addr)

    @staticmethod
    def _codegen_Type(node):
        if node.name == "int":
            return ir.IntType(32)

    @staticmethod
    def _codegen_Integer(node):
        return ir.Constant(ir.IntType(32), int(node.value))

    def generate(self, _ast):
        self.ast = _ast
        self.module = ir.Module(name=self.ast.name)
        self.generate_code(self.ast)
        print(self.module)
