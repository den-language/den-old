from .node import Node

# Functions AST nodes

class Function(Node):
    def __init__(self, name, pos_arguments, kw_arguments, block, position):
        self.position = position
        self.name = name
        self.pos_arguments = pos_arguments
        self.kw_arguments = kw_arguments
        self.block = block
