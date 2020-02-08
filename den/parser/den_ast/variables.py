from .node import Node

# Variable AST nodes


class variables:
    class VariableAssignFull(Node):
        def __init__(self, _type, _id, value, position):
            self.type = _type
            self.id = _id
            self.value = value
            self.position = position

    class VariableDec(Node):
        def __init__(self, _id, _type, position):
            self.id = _id
            self.type = _type
            self.position = position

    class VariableAssign(Node):
        def __init__(self, _id, value, position):
            self.id = _id
            self.value = value
            self.position = position
