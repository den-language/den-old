from .node import Node

# Maths AST nodes


class maths:
    class Add(Node):
        """Addition node."""

        def __init__(self, left, right, position):
            """
            Args:
                left (Expression): Left hand side of operation.
                right (Expression): Right hand side of operation.
                position (Location): Position of addition.
            """
            self.left = left
            self.right = right
            self.position = position

    class Sub(Node):
        """Subtraction node."""

        def __init__(self, left, right, position):
            """
            Args:
                left (Expression): Left hand side of operation.
                right (Expression): Right hand side of operation.
                position (Location): Position of subtraction.
            """
            self.left = left
            self.right = right
            self.position = position

    class Mul(Node):
        """Multiplication node."""

        def __init__(self, left, right, position):
            """
            Args:
                left (Expression): Left hand side of operation.
                right (Expression): Right hand side of operation.
                position (Location): Position of multiplication.
            """
            self.left = left
            self.right = right
            self.position = position

    class Div(Node):
        """Division node."""

        def __init__(self, left, right, position):
            """
            Args:
                left (Expression): Left hand side of operation.
                right (Expression): Right hand side of operation.
                position (Location): Position of divide.
            """
            self.left = left
            self.right = right
            self.position = position

    class Mod(Node):
        """Modulo node."""

        def __init__(self, left, right, position):
            """
            Args:
                left (Expression): Left hand side of operation.
                right (Expression): Right hand side of operation.
                position (Location): Position of modulo.
            """
            self.left = left
            self.right = right
            self.position = position

    class Neg(Node):
        """Negate/negative node."""

        def __init__(self, value, position):
            """
            Args:
                value (Expression): Value to be negated/turned negative.
                position (Location): Position of negate.
            """
            self.value = value
            self.position = position
