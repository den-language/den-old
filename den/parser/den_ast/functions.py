from .node import Node

# Functions AST nodes
class functions:
    class FunctionDefinition(Node):
        def __init__(self, return_type, name, arguments, block, position):
            self.return_type = return_type
            self.position = position
            self.name = name
            self.arguments = arguments
            self.block = block

    class Return(Node):
        def __init__(self, value, position):
            self.value = value
            self.position = position

    class Arguments(Node):
        def __init__(self, positional=None, keyword=None):
            self.positional_arguments = positional
            self.keyword_arguments = keyword

    class PositionalArguments(Node):
        def __init__(self, arguments):
            self.arguments = arguments

    class KeywordArguments(Node):
        def __init__(self, arguments):
            self.arguments = arguments
