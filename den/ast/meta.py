from .node import Node

class Block(Node):
    def __init__(self, statements):
        self.statements = statements

    def push(self, statement):
        self.statements.append(statement)
