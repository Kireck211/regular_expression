from sys import argv
from automata_lib import *
import codecs

script, file_name = argv

def m1(regular_expression):
	regular_expression = add_concats(regular_expression)
	return shunting_yard(regular_expression) 

def m2(postfix):
	afn_epsilon(postfix)
	print_stack()
	return stack

def main():
	input_file = codecs.open(file_name, encoding='utf-8')
	regular_expression = input_file.readline()
	module1 = m1(regular_expression)
	print("Module 1 (RPN): " + module1, end="\n\n")
	print("Module 2 (AFN-e):")
	module2 = m2(module1)
	m3()

main()