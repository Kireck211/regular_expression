from collections import deque
from sys import path, argv
sys.path.insert(0, '/path/to/regular_expression/lib')
from automata_lib import *

graph = []
script, file_name = argv

def m1(regular_expression):
	regular_expression = add_concats(regular_expression)
	shunting_yard(regular_expression)
	postfix = ""
	for token in deque:
		postfix += token.value
	return postfix 

def m2(postfix):
	initialize_graph(postfix)
	print(graph)
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
	print("M1: " + m1(regular_expression), end="")
	#m2(m1(regular_expression))


main()