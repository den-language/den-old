from .node import Node

# Functions AST nodes
class functions:
    class FunctionDefinition(Node):
        def __init__(self, return_type, name, arguments, block, position):
            self.position = position
            self.name = name
            self.arguments = arguments
            self.block = block

    class Arguments:
        def __init__(self, positional=None, keyword=None):
            self.positional_arguments = positional
            self.keyword_arguments = keyword

    class PositionalArguments:
        def __init__(self, arguments):
            self.arguments = arguments

    class KeywordArguments:
        def __init__(self, arguments):
            self.arguments = arguments
