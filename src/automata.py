from sys import argv
from automata_lib import *

script, file_name = argv

def m1(regular_expression):
	regular_expression = add_concats(regular_expression)
	return shunting_yard(regular_expression) 

def m2(postfix):
	initialize_graph(postfix)
	print_graph()
	#print(append_not_atom(graph[0], postfix))
	#print(append_not_atom(graph[0], postfix))

def main():
	input_file = open(file_name)
	regular_expression = input_file.readline()
	module1 = m1(regular_expression)
	print("Module 1 (RPN): " +module1)
	#m2(module1)


main()