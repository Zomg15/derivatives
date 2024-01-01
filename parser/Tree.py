class Tree:
    def __init__(self, name, left = None, right = None):
        self.name = name
        self.left = left
        self.right = right
        
    def children(self):
        return [self.left(), self.right()]
    
    def __eq__(self, other):
        return self.name == other.name and self.left == other.left and self.right == other.right
    
    def replace_left(self, tree):
        self.left = tree

    def replace_right(self, tree):
        self.right = tree

    def __repr__(self):
        '''if self.name in ["+", "-", "*", "/", "^"]:
            return f"{repr(self.left)} {self.name} {repr(self.right)}"
        else:
            return f"{self.name}({repr(self.left)}{',' if self.right is not None else ''}{f' {repr(self.right)}' if self.right is not None else ''})"'''
        
        return f"({repr(self.left)} {self.name} {repr(self.right)})"