from Tree import Tree

def brackets_match(tokenised_expression):
    depth = 0

    for token in tokenised_expression:
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
    
    return depth == 0


def parse(original_array):
    tree = original_array
    
    # If parentheses are mismatched, throw error
    if not brackets_match(tree):
        raise ValueError("Mismatched parentheses.")

    # Remove parentheses from beginning and end
    if tree[0] == "(" and tree[-1] == ")":
        del tree[0]
        del tree[-1]
    
    # If the top-level operation is a function, set that to the root of the tree and the rest to the branch, then parse that
    if tree[0] in ["sin", "cos", "tan", "log", "ln", "sqrt"] and tree[1] == "(" and tree[-1] == ")":
        if tree[0] == "sqrt":
            new_tree = Tree("^", tree[1:], 0.5)
            new_tree.replace_left(parse(new_tree.left))
            return new_tree
        else:
            new_tree = Tree(tree[0], tree[1:])
            new_tree.replace_left(parse(new_tree.left))
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
    for token, i in reversed(list(enumerate(tree))):
        if token == ")":
            depth += 1
            if not has_nested_parentheses:
                topmost_end_index = i
            has_nested_parentheses = True
        if token == "(":
            depth -= 1
        
        if depth == 0 and has_nested_parentheses: # Topmost brackets found
            if tree[i-1] in ["sin", "cos", "tan", "log", "ln", "sqrt"]:
                topmost_start_index = i - 1
            else:
                topmost_start_index = i
            topmost_parentheses = tree[topmost_start_index:topmost_end_index]
            del tree[topmost_start_index:topmost_end_index]
            tree.insert(topmost_start_index, parse(topmost_parentheses))
    
    return tree
        

parsed_tree = parse(['sqrt', '(', 'x', '^', '3', '+', '3.3', 'x', '^', '2', '+', '9', 'x', '/', 'sin', '(', 'x', ')', ')', '+', 'ln', '(', 'x', ')'])
print(parsed_tree)