from .node import Node

# Maths AST nodes

class Add(Node):
    def __init__(self, term1, term2):
        self.term1 = term1
        self.term2 = term2

class Sub(Node):
    def __init__(self, term1, term2):
        self.term1 = term1
        self.term2 = term2

class Mul(Node):
    def __init__(self, term1, term2):
        self.term1 = term1
        self.term2 = term2

class Div(Node):
    def __init__(self, term1, term2):
        self.term1 = term1
        self.term2 = term2

class Mod(Node):
    def __init__(self, term1, term2):
        self.term1 = term1
        self.term2 = term2
