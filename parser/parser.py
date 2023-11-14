def brackets_match(tokenised_expression):
    depth = 0

    for token in tokenised_expression:
        if token == "(":
            depth += 1
        elif token == ")":
            depth -= 1
    
    return depth == 0