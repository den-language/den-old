try:
    from parser import DenParser
    from lexer import DenLexer
    from codegen import ModuleCodeGen
except ImportError:
    from den.parser import DenParser
    from den.lexer import DenLexer
    from den.codegen import ModuleCodeGen


class DenModule:
    def __init__(self, filename, text=""):
        self.lexer = DenLexer()
        self.parser = DenParser()
        self.filename = filename
        self.text = text

    def generate(self):
        self.result = self.parser.parse(self.lexer.tokenize(self.text))
        self.result.add_name(self.filename)
        self.module = ModuleCodeGen()
        self.module.generate(self.result)

    def add_text(self, text):
        self.text = text
