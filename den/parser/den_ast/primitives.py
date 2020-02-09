from .node import Node


# Primitive AST nodes


class primitives:
    class Integer(Node):
        """Integer type."""

        def __init__(self, value, position):
            """
            Args:
                value (int): Value of integer.
                position (Location): Position of integer.
            """
            self.value = value
            self.position = position

    class String(Node):
        """String type."""

        def __init__(self, value, position):
            """
            Args:
                value (str): Value of string.
                position (Location): Position of string.
            """
            self.value = value
            self.position = position

    class Type(Node):
        """Type node."""

        def __init__(self, name, position):
            """
            Args:
                name (str): Name of type.
                position (Location): Position of type.
            """
            self.name = name
            self.position = position

    class NameID(Node):
        """Name ID node, for names."""

        def __init__(self, name, position, tp=None):
            """
            Args:
                name (str): Name of NameID.
                position (Location): Position of integer.
                tp (Type): Type of NameID.
            """
            self.name = name
            self.type = tp
            self.position = position

    class RefID(Node):
        """Reference to ID node."""

        def __init__(self, name, position):
            """
            Args:
                name (str): Name of referenced variable.
                position (Location): Position of integer.
            """
            self.name = name
            self.position = position
