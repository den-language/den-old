import llvmlite.binding as llvm


def initialize():
    llvm.initialize()
    llvm.initialize_native_asmprinter()
    llvm.initialize_native_target()


def compile_ir(llvm_ir):
    """
    Compile the LLVM IR string with the given engine.
    The compiled module object is returned.
    """

    target = llvm.Target.from_default_triple()
    target_machine = target.create_target_machine()
    mod = llvm.parse_assembly(str(llvm_ir))
    mod.verify()

    return mod, target_machine
