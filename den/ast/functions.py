from .node import Node

class Function(Node):
    def __init__(self, name, pos_arguments, kw_arguments, block):
        self.name = name
        self.pos_arguments = pos_arguments
        self.kw_arguments = kw_arguments
        self.block = block
