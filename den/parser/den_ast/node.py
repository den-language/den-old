# Base node class

class Node:
    def __str__(self):
        return f"{type(self).__name__}"
    
    def dump(self):
        raise NotImplementedError
