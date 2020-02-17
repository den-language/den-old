from .node import Node


class imports:
    class Import(Node):
        """Simple import statement."""

        def __init__(self, namespace, position):
            """
            Args:
                namespace (Namespace): Namespace to be imported.
                position (Location): Position of import.
            """
            self.namespace = namespace
            self.position = position
