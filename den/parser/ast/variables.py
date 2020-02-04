from .node import Node

# Variable AST nodes

class VariableDec:
    def __init__(self, _type, _id, value):
        self.type = _type
        self.id = _id
        self.value = value
        self.position = position

class VariableRef:
    def __init__(self, _id, value):
        self.id = _id
        self.position = position

class VariableAssign:
    def __init__(self, _id, value):
        self.id = _id
        self.value = value
        self.position = position
