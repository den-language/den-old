from llvmlite import ir
import os
from .generate_module import run_compile

try:
    import errors.errors as errors
    import parser.den_ast as dast
    from helpers.location import Location
except ImportError:
    import den.errors.errors as errors
    import den.parser.den_ast as dast
    from den.helpers.location import Location


class ModuleCodeGen:
    def __init__(self, logger, modules, path, _ast=None, debug=False):
        self.ast = _ast
        self.debug = debug
        self.module = None
        self.builder = None
        self.path = path

        self.result = None

        self.builtin_types = {}
        self.symtab = {}
        self.functions = []

        self.modules = modules

        self.logger = logger

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

        self.logger.log(f"Codegen: generating a {node}")
        return getattr(self, method)(node)

    # Expressions

    @staticmethod
    def _codegen_Integer(node):
        return ir.Constant(ir.IntType(32), int(node.value))

    def _codegen_Neg(self, node):
        return self.builder.neg(self._codegen(node.value), name="tmpneg")

    def _codegen_Import(self, node):
        import_path = list(
            filter(None, os.path.normpath(os.path.dirname(self.path)).split(os.sep))
        )

        for i, name in enumerate(node.namespace.ids):
            if os.path.isfile(
                os.path.join(
                    os.sep, os.path.join(*import_path), (filename := f"{name.name}.den")
                )
            ):
                import_path.append(filename)
            elif os.path.isdir(
                os.path.join(
                    os.sep,
                    os.path.join(*import_path),
                    (dirname := f"{name.name}{os.sep}"),
                )
            ):
                import_path.append(dirname)
            else:
                last_index = i
                break
            last_index = i

        module = run_compile(os.path.join(os.sep, *import_path), self.logger.debug)
        if len(node.namespace.ids[last_index:]) == 0:
            pass
        else:
            for name in node.namespace.ids[last_index:]:
                pass

    def _codegen_RefID(self, node):
        if node.name in self.symtab:
            variable = self.symtab[node.name]
            return self.builder.load(variable, node.name)
        else:
            self.logger.error(
                errors.undefined_variable_error,
                f"Use of undefined object `{node.name}` detected",
                node.position,
            )
            self.logger.throw()

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
            self.logger.error(
                errors.type_error,
                f"Conflicting types between `{left.type.__class__.__name__}` and `{right.type.__class__.__name__}`",
                left.position,
            )
            self.logger.throw()
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
                self._codegen(arg.type)
                for arg in node.arguments.positional_arguments.arguments
            ],
        )

        if funcname == "entry":
            funcname = "main"

        if funcname in self.module.globals:
            self.logger.error(
                errors.function_redefinition_error,
                f"Function `{funcname}` was redefined",
                node.position,
            )
            self.logger.throw()
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

        if node.block.__class__.__name__ == "Block":
            for statement in node.block.statements:
                if statement.__class__.__name__ == "Return" and node.return_none:
                    continue
                self._codegen(statement)

            if node.return_none:
                self._codegen_Return(
                    dast.functions.Return(
                        dast.primitives.Integer(0, Location(0, 0)), Location(0, 0)
                    )
                )

        else:
            self._codegen_Return(dast.functions.Return(node.block, Location(0, 0)))

        return func

    def _codegen_FunctionCall(self, node):
        try:
            called_function = self.module.get_global(node.name.name)
        except KeyError:
            self.logger.error(
                errors.undefined_function_error,
                f"Function `{node.name.name}` is undefined",
                node.position,
            )
            self.logger.throw()
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

        if node.id.name in self.symtab:
            var_addr = self.symtab[node.id.name]
        elif node.id.name not in self.symtab:
            self.logger.error(
                errors.uninitialized_variable_error,
                f"Variable `{node.id.name}` is assigned before its initialization",
                node.position,
            )
            self.logger.throw()

        self.builder.position_at_end(saved_block)
        self.builder.store(init_val, var_addr)

    @staticmethod
    def _codegen_Type(node):
        if node.name == "int":
            return ir.IntType(32)

    def generate(self, _ast):
        self.ast = _ast
        self.module = ir.Module(name=self.ast.name)
        self.generate_code(self.ast)

        self.logger.log(f"Codegen: Generated LLVM IR: \n{self.module}")

        return self.module
