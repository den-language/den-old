from .node import Node

# Variable AST nodes


class variables:
    class VariableAssignFull(Node):
        """Full variable assign, with type, value, and ID."""

        def __init__(self, _type, _id, value, position):
            """
            Args:
                _type (Type): Type of variable.
                _id (NameID): Name of variable.
                value (Expression): Expression assigned to variable.
                position (Location): Position of full variable assign.
            """
            self.type = _type
            self.id = _id
            self.value = value
            self.position = position

    class VariableDec(Node):
        """Variable declaration with ID and type."""

        def __init__(self, _id, _type, position):
            """
            Args:
                _id (NameID): Name of variable.
                _type (Type): Type of variable.
                position (Location): Position of full variable assign.
            """
            self.id = _id
            self.type = _type
            self.position = position

    class VariableAssign(Node):
        """Variable assignment with ID and value."""

        def __init__(self, _id, value, position):
            """
            Args:
                _id (NameID): Name of variable.
                value (Expression): Expression assigned to variable.
                position (Location): Position of full variable assign.
            """
            self.id = _id
            self.value = value
            self.position = position
