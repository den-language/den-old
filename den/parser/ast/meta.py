from .node import Node

# Meta code sections

class Program(Node):
    def __init__(self, block):
        self.block = block
        self.position = position

class Block(Node):
    def __init__(self, statements):
        self.statements = statements
        self.position = position

    def push(self, statement):
        self.statements.append(statement)
