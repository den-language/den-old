from .node import Node

# Variable AST nodes

class VariableDec:
    def __init__(self, _type, _id, value):
        self.type = _type
        self.id = _id
        self.value = value

class VariableRef:
    def __init__(self, _id, value):
        self.id = _id

class VariableAssign:
    def __init__(self, _id, value):
        self.id = _id
        self.value = value
