from .node import Node

# Variable AST nodes

class variables:
    class VariableAssign:
        def __init__(self, _type, _id, value, position):
            self.type = _type
            self.id = _id
            self.value = value
            self.position = position
