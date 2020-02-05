from .node import Node

# Meta code sections

class meta:
    class Program(Node):
        def __init__(self, block, position):
            self.block = block
            self.position = position

    class Block(Node):
        def __init__(self, statements, position):
            self.statements = statements
            self.position = position

        def push(self, statement):
            self.statements.append(statement)
