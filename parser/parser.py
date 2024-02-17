from parser.Tree import Tree

class Parser:
    def brackets_match(self, tokenised_expression):
        depth = 0

        for token in tokenised_expression:
            if token == "(":
                depth += 1
            elif token == ")":
                depth -= 1
        
        return depth == 0
    
    def is_number(self, token):
        try:
            _ = float(token)
        except Exception:
            return False
        return True

    def begin_parse(self, arr):
        return Tree("f", self.parse(arr))

    def parse(self, original_array):
        tree = original_array
        
        # If parentheses are mismatched, throw error
        if not self.brackets_match(tree):
            raise ValueError("Mismatched parentheses.")

        # Remove parentheses from beginning and end
        if tree[0] == "(":
            depth = 0
            end_index = 0
            for i, token in enumerate(tree):
                if token == "(":
                    depth += 1
                if token == ")":
                    depth -= 1
                if depth == 0:
                    end_index = i
                    break
            
            if end_index == len(tree) - 1:
                del tree[0]
                del tree[-1]
        print(f"currently parsing: {tree}")
        # If the top-level operation is a function, set that to the root of the tree and the rest to the branch, then parse that
        if tree[0] in ["sin", "cos", "tan", "log", "ln", "sqrt"] and tree[1] == "(":
            print("function found at beginning")
            depth = 0
            end_index = 0
            has_nested_parentheses = False
            for i, token in enumerate(tree):
                print(i, token)
                if token == "(":
                    print("( found at sqrt")
                    has_nested_parentheses = True
                    depth += 1
                if token == ")":
                    print(") found at sqrt")
                    depth -= 1
                if depth == 0 and has_nested_parentheses:
                    end_index = i
                    break
            print(end_index)
            if end_index == len(tree) - 1:
                if tree[0] == "sqrt":
                    new_tree = Tree("^", tree[1:(end_index+1)], 0.5)
                    new_tree.replace_left(self.parse(new_tree.left))
                    return new_tree
                else:
                    print(f"new tree: {tree[1:(end_index+1)]}")
                    new_tree = Tree(tree[0], tree[1:(end_index+1)])
                    new_tree.replace_left(self.parse(new_tree.left))
                    return new_tree


        # Otherwise, go through list (in reverse order, to not affect later indices).
        # If an opening parenthesis is met, store the index, and start counting bracket depth.
        # Once zero bracket depth is reached, take the read tokens and combine them into one array, replacing the run with it.
        # If there is a function token before the parentheses, add that as well.
        # Run the parse function on that array.
        # Keep iterating until the end is reached.
        
        depth = 0
        has_nested_parentheses = False
        topmost_end_index = 0
        topmost_start_index = 0
        print("parsing parentheses")
        for i, token in reversed(list(enumerate(tree))):
            if token == ")":
                print(") found")
                depth += 1
                if not has_nested_parentheses:
                    topmost_end_index = i
                has_nested_parentheses = True
            if token == "(":
                print("( found")
                depth -= 1
            
            if depth == 0 and has_nested_parentheses: # Topmost brackets found
                if tree[i-1] in ["sin", "cos", "tan", "log", "ln", "sqrt"]:
                    topmost_start_index = i - 1
                else:
                    topmost_start_index = i
                print(topmost_start_index, topmost_end_index)
                topmost_parentheses = tree[topmost_start_index:topmost_end_index+1]
                del tree[topmost_start_index:topmost_end_index+1]
                tree.insert(topmost_start_index, self.parse(topmost_parentheses))
                has_nested_parentheses = False
        
        # Turn x into a polynomial
        
        print("polynomie time")
        for i, token in enumerate(tree):
            if token == "x":
                print(f"found x at {i}")
                coefficient = 1
                power = 1
                has_coefficient = False
                has_power = False
                if i != 0 and self.is_number(tree[i-1]):
                    print(f"found coefficient at {i-1}: {tree[i-1]}")
                    coefficient = float(tree[i-1])
                    has_coefficient = True
                if i < len(tree) - 1 and self.is_number(tree[i+1]):
                    print(f"found power at {i+1}: {tree[i+1]}")
                    power = float(tree[i+1])
                    has_power = True
                polynomial_tree = Tree("x", coefficient, power)
                del tree[(i-1 if has_coefficient else i):(i+2 if has_power else i+1)]
                tree.insert(i-1 if has_coefficient else i, polynomial_tree)
                


        # Now that parentheses are dealt with, we can do the operations
        # Go by order of operations (exponents, multiplication/division, addition/subtraction), bring together left and right operands
        # When deleting operator and left/right branches, the index you have to reinsert the tree in is index - 1 (the place of the left operand)
        
        print("parsing operations")
        operation_phase = 0
        operators = [["^"], ["*", "/"], ["+", "-"]]
        while operation_phase <= 2:
            for i, token in enumerate(tree):
                if type(token) is str and token in operators[operation_phase]:
                    print(f"found operator {token}")
                    print(f"left operand: {tree[i-1]}")
                    print(f"right operand: {tree[i+1]}")
                    operation_tree = Tree(token, tree[i-1], tree[i+1])
                    del tree[i-1:i+2]
                    tree.insert(i-1, operation_tree)
            operation_phase += 1

        if type(tree) is list:
            print(f"ended up with list {tree}")
            return tree[0]
        else:
            print(f"returning {tree}")
            return tree
        
# sqrt(x) + ln(x+1)
#parser = Parser()
#parsed_tree = parser.begin_parse(['sqrt', '(', 'x', ')', '+', 'ln', '(', 'x', '+', '1', ')'])
#print(parsed_tree)
#print("pretty", parsed_tree.pretty())