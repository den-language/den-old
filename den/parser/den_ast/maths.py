from .node import Node

# Maths AST nodes
class maths:
    class Add(Node):
        def __init__(self, left, right, position):
            self.left = left
            self.right = right
            self.position = position

    class Sub(Node):
        def __init__(self, left, right, position):
            self.left = left
            self.right = right
            self.position = position

    class Mul(Node):
        def __init__(self, left, right, position):
            self.left = left
            self.right = right
            self.position = position

    class Div(Node):
        def __init__(self, left, right, position):
            self.left = left
            self.right = right
            self.position = position

    class Mod(Node):
        def __init__(self, left, right, position):
            self.left = left
            self.right = right
            self.position = position

    class Neg(Node):
        def __init__(self, value, position):
            self.value = value
            self.position = position
