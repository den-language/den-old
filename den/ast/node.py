# Base node class
class Node:
    def __init__(self, name, children, value=""):
        self.name = name
        self.children = children
        self.value = value
