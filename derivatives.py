from tokenizer import Tokenizer
from parser.parser import Parser
from find_derivative import FindDerivative

func = input("Insert function: ")

tokeniser = Tokenizer()

tokeniser.run(func)

result = tokeniser.result

parser = Parser()

tree_form = parser.begin_parse(result)

print(tree_form)

derivative_finder = FindDerivative()

derivative = derivative_finder.derive(tree_form)

print(derivative)