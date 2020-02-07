from .node import Node
from llvmlite import ir


# Primitive AST nodes


class primitives:
    class Integer(Node):
        def __init__(self, value, position):
            self.value = value
            self.position = position

    class String(Node):
        def __init__(self, value, position):
            self.value = value
            self.position = position

    class Type(Node):
        def __init__(self, name, position):
            self.name = name
            self.position = position

    class NameID(Node):
        def __init__(self, name, position):
            self.name = name
            self.position = position

    class RefID(Node):
        def __init__(self, name, position):
            self.name = name
            self.position = position
