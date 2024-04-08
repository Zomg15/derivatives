class Tree:
    def __init__(self, name, left = None, right = None):
        self.name = name
        self.left = left
        self.right = right

    def is_number(self, token):
        try:
            _ = float(token)
        except Exception:
            return False
        return True
        
    def children(self):
        return [self.left(), self.right()]
    
    def __eq__(self, other):
        if type(other) != Tree:
            return False
        return self.name == other.name and self.left == other.left and self.right == other.right
    
    def replace_left(self, tree):
        self.left = tree

    def replace_right(self, tree):
        self.right = tree

    def display_number(self, num):
        return int(num) if num.is_integer() else num

    def __repr__(self):
        if self.name in ["+", "-", "*", "/", "^"]:
            return f"({repr(self.left)} {self.name} {repr(self.right)})".replace("'", "")
        elif self.name == "x":
            if self.left == 1.0 and self.right == 1.0:
                return "x"
            elif self.right == 1.0:
                return f"{self.display_number(self.left)}x"
            elif self.left == 1.0:
                return f"x^{self.display_number(self.right)}"
            else:
                return f"{self.display_number(self.left)}x^{self.display_number(self.right)}"
        else:
            return f"{self.name}({repr(self.left)}{',' if self.right is not None else ''}{f' {repr(self.right)}' if self.right is not None else ''})".replace("'", "")
    
    def find_and_replace(self, find, replace):
        tree_to_find = find
        tree_to_replace = replace
        if self.left == tree_to_find:
            self.replace_left(replace)
        elif type(self.left) is Tree:
            self.left.find_and_replace(tree_to_find, tree_to_replace)
        
        if self.right == find:
            self.replace_right(replace)
        elif type(self.right) is Tree:
            self.right.find_and_replace(tree_to_find, tree_to_replace)

    def clean(self, tree): # This should only be run after the derivative is found.
        if type(tree) != Tree:
            if self.is_number(tree):
                return float(tree)
            else:
                return tree
        
        if tree.name != "x":
            tree.replace_left(tree.clean(tree.left))
            if tree.right is not None:
                tree.replace_right(tree.clean(tree.right))

        match tree.name:
            case "+":
                if self.is_number(tree.left) and self.is_number(tree.right):
                    return float(tree.left) + float(tree.right)
                else:
                    if tree.left == 0:
                        return tree.right
                    if tree.right == 0:
                        return tree.left
            case "-":
                if self.is_number(tree.left) and self.is_number(tree.right):
                    return float(tree.left) - float(tree.right)
                else:
                    if tree.left == 0:
                        return Tree("*", -1, tree.right)
                    if tree.right == 0:
                        return tree.left
            case "*":
                if self.is_number(tree.left) and self.is_number(tree.right):
                    return float(tree.left) * float(tree.right)
                else:
                    if tree.left == 0 or tree.right == 0:
                        return 0
                    if tree.left == 1:
                        return tree.right
                    if tree.right == 1:
                        return tree.left
            case "/":
                if self.is_number(tree.left) and self.is_number(tree.right):
                    return float(tree.left) * float(tree.right)
                else:
                    if tree.left == 0:
                        return 0
                    if tree.right == 1:
                        return tree.left
        return tree

        
        