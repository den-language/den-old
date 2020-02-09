try:
    from parser import DenParser
    from lexer import DenLexer
    from codegen import ModuleCodeGen
    from errors.logger import Logger
except ImportError:
    from den.parser import DenParser
    from den.lexer import DenLexer
    from den.codegen import ModuleCodeGen
    from den.errors.logger import Logger


class DenModule:
    def __init__(self, filename, text=""):
        self.lexer = DenLexer()
        self.parser = DenParser()
        self.filename = filename
        self.text = text
        self.logger = Logger("test.den", text, debug=True)
        self.parser.set_logger(self.logger)
        self.lexer.set_logger(self.logger)

    def generate(self):
        tokens = self.lexer.tokenize(self.text)
        self.result = self.parser.parse(tokens)
        self.logger.throw()
        self.result.add_name(self.filename)
        self.module = ModuleCodeGen(self.logger)
        self.module.generate(self.result)
        self.logger.throw()

    def add_text(self, text):
        self.text = text
