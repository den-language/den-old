from .node import Node
import uuid


# Meta code sections


class meta:
    class Program(Node):
        """Master program node."""

        def __init__(self, block, position, name=None):
            """
            Args:
                block (Block): Block in program.
                position (Location): Position of program.
                name (str): Name of file.
            """
            self.block = block
            if name is None:
                self.name = f"{uuid.uuid4()}"
            else:
                self.name = "_".join(name.split(".")[:-1])
            self.position = position

        def add_name(self, name):
            """
            Input new filename.

            Args:
                name (str): Name of file.
            """
            self.name = "_".join(name.split(".")[:-1])

    class Block(Node):
        """Block of code node."""

        def __init__(self, statements, position):
            """
            Args:
                statements (list): List if statements.
                position (Location): Position of block.
            """
            self.statements = statements
            self.position = position
            self.label = None  # e.g. entry

        def push(self, statement):
            """
            Push a statement to the statements list.

            Args:
                statement (Statement): Statement to add to statements.
            """

            self.statements.append(statement)
