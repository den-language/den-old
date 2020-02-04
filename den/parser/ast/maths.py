from .node import Node

# Maths AST nodes

class Add(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.position = position

class Sub(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.position = position

class Mul(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.position = position

class Div(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.position = position

class Mod(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.position = position
