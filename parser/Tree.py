class Tree:
    def __init__(self, name, left = None, right = None):
        self.name = name
        self.left = left
        self.right = right
    
    def left(self):
        return self.left
        
    def right(self):
        return self.right
        
    def children(self):
        return [self.left(), self.right()]
    
    def __eq__(self, other):
        return self.name == other.name and self.left == other.left and self.right == other.right
    
    def replace_left(self, tree):
        self.left = tree

    def replace_right(self, tree):
        self.right = tree