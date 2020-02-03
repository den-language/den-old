from .node import Node

class Function(Node):
    def __init__(self, name, block):
        self.name = name
        self.block = block
