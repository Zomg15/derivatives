special_characters = "()+-*/^ex"
number_characters = "1234567890."

class Tokenizer:
    index = 0
    expression = ""
    result = []

    # Returns the current character
    def current(self):
        return self.expression[self.index]
    
    # Returns the current character and moves to the next one
    def consume(self):
        result = self.expression[self.index]
        self.index += 1
        return result
    
    def tokenize_number(self):
        result = ""
        # Checks if the number contains a decimal.
        is_decimal = False
        # Continues with the iteration until a non-numeric character is reached.
        while self.index < len(self.expression) and self.current() in number_characters:
            if self.current() == ".":
                if not is_decimal:
                    is_decimal = True
                else:
                    raise ValueError("multiple decimal places in number")
            result += self.consume()
        self.append_if_exists(result)
    
    # Adds the string as a token to the array, if it exists
    def append_if_exists(self, token):
        if len(token) > 0:
            self.result.append(token)
    
    def run(self, source):
        self.expression = source.replace(" ", "")
        current_token = ""

        # Loop until all characters in the expression have been checked
        while self.index < len(self.expression):
            # If there's a special character, add the current run as a token, and then add the special character
            if self.current() in special_characters:
                self.append_if_exists(current_token)
                current_token = ""
                self.append_if_exists(self.consume())
            # If there's a number character, add the current run as a token, and run the special number tokenizer
            elif self.current() in number_characters:
                self.append_if_exists(current_token)
                current_token = ""
                self.tokenize_number()
            # Otherwise, it's probably just a function name, so make it a token
            else:
                current_token += self.consume()

tokenizer = Tokenizer()
tokenizer.run("sqrt(x^3 + 3.3x^2 + 9x/ sin(x)) + ln(x)")
print(tokenizer.result)