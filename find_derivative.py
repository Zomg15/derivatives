from parser.Tree import Tree

class FindDerivative:

    # 1x^1, aka the identity function
    x = Tree("x", 1.0, 1.0)

    def derive(self, original: Tree):
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
                if original.left == "e":
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
                # Composite exponential - get back here when chain rule is done!
                else:
                    raise ValueError("Not implemented yet!")
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
                            1,
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
            # Chain rule
            else:
                raise ValueError("Not implemented yet!")
        
