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
            tree = Tree("^", tree[1:], 0.5)
            tree.replace_left(parse(tree.left()))
            return tree
        else:
            tree = Tree(tree[0], tree[1:])
            tree.replace_left(parse(tree.left()))
            return tree


    # Otherwise, go through list (in reverse order, to not affect later indices).
    # If an opening parenthesis is met, store the index, and start counting bracket depth.
    # Once zero bracket depth is reached, take the read tokens and combine them into one array, replacing the run with it.
    # If there is a function token before the parentheses, add that as well.
    # Run the parse function on that array.
    # Keep iterating until the end is reached.
    