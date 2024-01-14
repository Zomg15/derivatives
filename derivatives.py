from tokenizer import Tokenizer
from parser.parser import Parser

func = input("Insert function: ")

tokeniser = Tokenizer()

tokeniser.run(func)

result = tokeniser.result

parser = Parser()

tree_form = parser.begin_parse(result)

print(tree_form)