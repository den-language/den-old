import os

try:
    from parser import DenParser
    from lexer import DenLexer
    from codegen import ModuleCodeGen
    from errors.logger import Logger
    from helpers.color import Color
    from helpers.llvm_gen import compile_ir
except ImportError:
    from den.parser import DenParser
    from den.lexer import DenLexer
    from den.codegen import ModuleCodeGen
    from den.errors.logger import Logger
    from den.helpers.color import Color
    from den.helpers.llvm_gen import compile_ir


class DenModule:
    def __init__(self, filename, abspath, output, text="", debug=False):
        self.lexer = DenLexer()
        self.parser = DenParser()
        self.ir = None

        self.filename = filename
        self.output_file = os.path.abspath("build/a.out") if output is None else output

        self.fullpath = abspath
        self.text = text
        self.logger = Logger(self.fullpath, text, debug=debug)

        self.modules = {}
        self.to_link = []

        self.parser.set_logger(self.logger)
        self.lexer.set_logger(self.logger)

    def generate(self):

        relpath = os.path.relpath(self.fullpath)

        self.logger.log("Started Lexing")
        self.logger.status(f"{Color.BOLD}{Color.GREEN}Lexing{Color.RESET} {relpath}")

        tokens = self.lexer.tokenize(self.text)

        self.logger.log("Started Parsing")
        self.logger.status(f"{Color.BOLD}{Color.GREEN}Parsing{Color.RESET} {relpath}")

        self.result = self.parser.parse(tokens)
        self.logger.throw()

        self.result.add_name(self.filename)

        self.logger.log("Started Codegen")
        self.logger.status(
            f"{Color.BOLD}{Color.GREEN}Generating{Color.RESET} {relpath}"
        )

        self.output = (
            f"{os.path.join(os.path.dirname(self.output_file), self.result.name)}.o"
        )
        self.to_link.append(self.output)

        self.module = ModuleCodeGen(
            self.logger, self.modules, self.fullpath, self.output, self.to_link
        )
        self.ir = self.module.generate(self.result)
        self.logger.throw()

    def write(self):
        self.logger.status(
            f"{Color.BOLD}{Color.GREEN}Writing to{Color.RESET} {os.path.relpath(self.output)}"
        )

        # Generate object file that is linked to excecutable
        mod, target_machine = compile_ir(self.ir)

        if not os.path.exists(os.path.dirname(self.output)):
            os.makedirs(os.path.dirname(self.output))

        with open(f"{self.output}", "wb+") as o:
            o.write(target_machine.emit_object(mod))

    def add_text(self, text):
        self.text = text
