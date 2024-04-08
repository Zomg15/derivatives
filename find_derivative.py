from parser.Tree import Tree

class FindDerivative:

    # 1x^1, aka the identity function
    x = Tree("x", 1.0, 1.0)

    def derive(self, original: Tree):
        # If it's a string, then it's probably a constant, meaning its derivative is 0
        if type(original) == str:
            return 0
        # Top-level function
        if original.name == "f":
            return self.derive(original.left)
        # Sum
        if original.name == "+":
            return Tree("+", self.derive(original.left), self.derive(original.right))
        # Product
        elif original.name == "*":
            # Multiplying by a constant
            if isinstance(original.left, (int, float)):
                return Tree("*", original.left, self.derive(original.right))
            elif isinstance(original.right, (int, float)):
                return Tree("*", original.right, self.derive(original.left))
            else:
                return Tree(
                    "+",
                    Tree(
                        "*",
                        self.derive(original.left),
                        original.right
                    ),
                    Tree(
                        "*",
                        original.left,
                        self.derive(original.right)
                    )
                )
        # Quotient
        elif original.name == "/":
            return Tree(
                "/",
                Tree(
                    "-",
                    Tree(
                        "*",
                        self.derive(original.left),
                        original.right
                    ),
                    Tree(
                        "*",
                        original.left,
                        self.derive(original.right)
                    )
                ),
                Tree("^", original.right, 2)
            )
        # Monomial
        elif original.name == "x":
            # For degree 1 monomials, just return the coefficient
            if original.right == 1.0:
                return original.left
            else:
                return Tree(
                    "x",
                    original.left * original.right,
                    original.right - 1
                )
        # If it got past those, then it's a unary function.
        else:
            # Exponentials
            if original.name == "^":
                # e^x
                if original.left == "e" and original.right == self.x:
                    return Tree("^", "e", self.x)
                # Non-composite exponential
                elif original.right == self.x:
                    return Tree(
                        "*",
                        original,
                        Tree(
                            "ln",
                            original.left
                        )
                    )
                # Composite exponential
                else:
                    if original.left == "e":
                        return Tree(
                            "*",
                            original,
                            self.derive(original.right)
                        )
                    else:
                        return Tree(
                            "*",
                            Tree(
                                "*",
                                original,
                                Tree(
                                    "ln",
                                    original.left
                                )
                            ),
                            self.derive(original.right)
                        )
            # ACTUAL unary functions - non-composite
            elif original.right is None and original.left == self.x:
                match original.name:
                    case "sin":
                        return Tree("cos", self.x)
                    case "cos":
                        return Tree("*", -1.0, Tree("sin", self.x))
                    case "tan":
                        return Tree(
                            "/",
                            1.0,
                            Tree(
                                "^",
                                Tree(
                                    "cos",
                                    self.x
                                ),
                                2.0
                            )
                        )
                    case "ln":
                        return Tree("/", 1.0, self.x)
                    case "log":
                        return Tree(
                            "/",
                            1.0,
                            Tree(
                                "*",
                                self.x,
                                Tree(
                                    "ln",
                                    10.0
                                )
                            )
                        )
                    case "sqrt":
                        return Tree(
                            "/",
                            1.0,
                            Tree(
                                "*",
                                2.0,
                                Tree(
                                    "sqrt",
                                    self.x
                                )
                            )
                        )
            # Chain rule
            else:
                outer_function = original
                inner_function = original.left
                outer_function.find_and_replace(inner_function, self.x)
                outer_function = self.derive(outer_function)
                outer_function.find_and_replace(self.x, inner_function)
                return Tree(
                    "*",
                    outer_function,
                    self.derive(inner_function)
                )
        
