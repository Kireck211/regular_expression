from collections import deque
from sys import argv
from automata_lib import *

script, file_name = argv

def m1(regular_expression):
	regular_expression = add_concats(regular_expression)
	return shunting_yard(regular_expression) 

def m2(postfix):
	initialize_graph(postfix)
	print(append_not_atom(graph[0], postfix))
	print(append_not_atom(graph[0], postfix))
	"""
	graph = create_graph(postfix)
	stack = []
	inital_node = Node(len(graph) - 1)
	initial_node.initial = True
	graph.append(initial_node)
	final_node = Node(len(graph) - 1)
	final_node.finalll = True
	for token in postfix:
		priority = return_priority(token)
		if (priority < 0):
			stack.append(token)
		else:
			add_node(token,)"""

def main():
	input_file = open(file_name)
	regular_expression = input_file.readline()
	module1 = m1(regular_expression)
	print("Module 1 (RPN): " +module1)
	m2(module1)


main()