from .node import Node
from .primitives import primitives


# Functions AST nodes


class functions:
    class FunctionDefinition(Node):
        """Function definition class."""

        def __init__(self, name, public, arguments, block, position, return_type=None):
            """
            Args:
                name (NameID): Name of function
                public (bool): Weather function is public or private
                arguments (Arguments): Arguments the function takes
                block (Block): Block of code to be run (or expression)
                position (Location): Position of function definition
                return_type (Type): Return type of function
            """
            if return_type is None:
                self.return_type = primitives.Type("int", position)
                self.return_none = True
            else:
                self.return_type = return_type
                self.return_none = False

            self.position = position
            self.name = name
            self.arguments = arguments
            self.block = block
            self.public = public

    class FunctionCall(Node):
        """Function call class."""

        def __init__(self, name, arguments, position):
            """
            Args:
                name (NameID): Name of function.
                arguments (Arguments): Arguments to pass to the function.
                position (Location): Position of function call.
            """
            self.position = position
            self.name = name
            self.arguments = arguments

    class Return(Node):
        """Return statement."""

        def __init__(self, value, position):
            """
            Args:
                value (Expression): Value to be returned.
                position (Location): Position of return statement.
            """
            self.value = value
            self.position = position

    class Arguments(Node):
        """Arguments class."""

        def __init__(self, positional=None, keyword=None):
            """
            Args:
                positional (PositionalArguments): Positional arguments.
                keyword (KeywordArguments): Keyword arguments.
            """
            self.positional_arguments = positional
            self.keyword_arguments = keyword

    class PositionalArguments(Node):
        """Positional arguments class."""

        def __init__(self, arguments):
            """
            Args:
                arguments (list): Positional arguments.
            """
            self.arguments = arguments

    class KeywordArguments(Node):
        """Keyword arguments class."""

        def __init__(self, arguments):
            """
            Args:
                arguments (list): Keyword arguments.
            """
            self.arguments = arguments
