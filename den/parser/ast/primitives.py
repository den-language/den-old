from .node import Node

# Primitive AST nodes

class Integer(Node):
    def __init__(self, value):
        self.value = value
        self.position = position

class String(Node):
    def __init__(self, value):
        self.value = value
        self.position = position
