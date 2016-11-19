from collections import deque
import copy

# ---------------- Classes ----------------

""" Class used to convert a character
	into an object containing token
	and priority value"""
class Token(object):
	"""Creates a token object"""
	def __init__(self, token):
		self.value = token
		priority = return_priority(token)
		self.priority = priority

""" Class used to create nodes and the transitions,
	all the transitions must have a key (character)
	and a list of states"""
class Node(object):
	"""Creates a node object"""
	def __init__(self):
		global count
		index = count
		count += 1
		self.index = index
		self.transitions = {}
		self.initial = False
		self.final = False
		self.visited = False

	def increment_index_count(self):
		global count
		count += 1
		self.index = count

""" Class used to show logical errors and exit the program """
class Errors(object):
	"""Creates an object with all the posibles bugs"""
	def __init__(self):
		self.errors = [
			'A postfix has a \"(\" or \")\"', 
			'Postfix was not well build, trying to pop of empty stack', 
			'Cannot remove key_transition, because transition is not in the left_node',
			'This final node has transitions',
			'The parent cannot be the same as the child in the bfs search_last_node mode'
		]

	def print_error(self, index):
		print(self.errors[index-1])
		exit(index)

""" Class used to add initial and last to the stack """
class GraphStack(object):
	""" Creates an object for the stack """
	def __init__(self, initial, last):
		self.initial = initial
		self.last = last

# ---------------- Classes ----------------




# ---------------- Global variables  ----------------

# Global priority operators indexes
operator_priority = [["(", ")"],["*","+"], [".", ","]];

# Global stack variable
stack = []

# Global counter of nodes
count = 0

# Global errors object
logical_errors = Errors()

# ---------------- Global variables  ----------------




# ---------------- Functions ----------------

""" Snippet function to print a list"""
def print_list(list):
	#print(len(list))
	for item in list:
		print(item.value, end="")
	print("")

""" Functionts that returns the priority value
	from -1 to 2 depending on indexes of operators
	declared in operators"""
def return_priority(operator):
	for index, operators in enumerate(operator_priority):
		if operator in operators:
			return index
	return -1

""" Funtion that returns a string with
	all the possible concats"""
def add_concats(regular_expression):
	new_regular_expression = []
	for i in range(0, len(regular_expression) - 1):
		new_regular_expression.append(regular_expression[i])
		if (regular_expression[i].isalpha()):
			if(regular_expression[i+1].isalpha()):
				new_regular_expression.append(".")
			elif(return_priority(regular_expression[i+1]) < 0):
				new_regular_expression.append(".")
			elif(regular_expression[i+1] == '('):
				new_regular_expression.append(".")
		elif (regular_expression[i] == ')'):
			if (regular_expression[i+1] == '('):
				new_regular_expression.append(".")
			elif(return_priority(regular_expression[i+1]) < 0):
				new_regular_expression.append(".")
		elif (return_priority(regular_expression[i]) > 0 and return_priority(regular_expression[i]) < 2):
			if (regular_expression[i+1].isalpha()):
				new_regular_expression.append(".")
			if (regular_expression[i+1] == '('):
				new_regular_expression.append(".")
		elif (return_priority(regular_expression[i]) < 0):
			if(return_priority(regular_expression[i+1]) < 0):
				new_regular_expression.append(".")

	new_regular_expression.append(regular_expression[len(regular_expression)-1])
	return "".join(new_regular_expression)

""" Function that returns a string from a deque"""
def token_to_string(deque):
	rpn = ""
	for item in deque:
		rpn += item.value
	return rpn

""" Functions that add to the deque a rpn
	(reversed polish notation) of a 
	regular expression"""
def shunting_yard(regular_expression):
	deque_sy = deque([])
	stack = []
	for token in regular_expression:
		token = Token(token)
		if (token.priority < 0):
			#print("Entra con letra o con caracter especial")
			deque_sy.append(token)
		elif (token.priority == 0):
			if (token.value == '('):
				#print("Entra con paréntesis (")
				stack.append(token)
			else:
				#print("Entra con paréntesis)")
				lookToken = stack.pop();
				while(lookToken.value != '('):
					deque_sy.append(lookToken)
					#print("Value token before pop: " + lookToken.value + " and size of stack: " + str(len(stack)))
					lookToken = stack.pop()
		else:
			#print("Entra con " + token.value)
			#print("Valor de comparacion: " + (stack[len(stack)-1].value) if len(stack) else 'pila vacia')
			while(len(stack) and stack[len(stack)-1].priority <= token.priority and stack[len(stack) - 1].value != '('): 
				#print("Top value of stack: " + stack[len(stack)-1].value +" and taken token: " + token.value)
				deque_sy.append(stack.pop())
			stack.append(token)
	while(len(stack)):
		deque_sy.append(stack.pop())
	return token_to_string(deque_sy)

""" Function that returns true 
	if the characters is an 
	atom, false otherwise"""
def is_atom(characters):
	if (return_priority(characters) < 0):
		return True
	return False

""" Function that prints all the graph and its transitions"""
def print_stack():
	print("The length of the stack: " + str(len(stack)))
	for graph in stack:
		bfs_iterative(stack[0].initial, 'print', None, None)


""" Function that adds a transition from the left_node 
	to the right_node with the a token transition"""
def add_transition(left_node, right_node, token):
	if (not token in left_node.transitions):
		left_node.transitions[token] = []
	left_node.transitions[token].append(right_node)


""" Function that removes transition with the value 
	of key_transition from left_node 
	to right_node"""
def remove_transition(left_node, right_node, key_transition):
	if (not key_transition in left_node.transitions):
		logical_errors.print_error(3)
	left_node.transitions[key_transition].remove(right_node)

def exchange_nodes(src_node, key_transition, goal_node, new_goal_node):
	src_node.transitions[key_transition].remove(goal_node)
	add_transition(src_node, new_goal_node, key_transition)

def bfs_iterative(node, mode, goal_node, new_goal_node):
	to_visit = deque([])
	to_visit.append(node)
	if(mode == 'print'):
		while(len(to_visit)):
			node_to_visit = to_visit.popleft()
			node_to_visit.visited = True			
			print("The node {} hast the next transitions:".format(node_to_visit.index))
			for key in node_to_visit.transitions:
				print("'{}': ".format(key), end="")
				for next_node in node_to_visit.transitions[key]:
					print("{}".format(next_node.index), end=" ")
					if(not next_node.visited and not next_node in to_visit):
						to_visit.append(next_node)
			print("")
		bfs_iterative(node, 'clear_visited', None, None)

	elif(mode == 'clear_visited'):
		while(len(to_visit)):
			node_to_visit = to_visit.popleft()
			node_to_visit.visited = False			
			for key in node_to_visit.transitions:
				for next_node in node_to_visit.transitions[key]:
					if(next_node.visited and not next_node in to_visit):
						to_visit.append(next_node)

	elif(mode == 'search_last_node'):
		while(len(to_visit)):
			node_to_visit = to_visit.popleft()
			node_to_visit.visited = True
			for key in node_to_visit.transitions:
				for next_node in node_to_visit.transitions[key]:
					if(not next_node.visited and not next_node in to_visit):
						if(next_node == goal_node):
							#print("From {} with {} key value the {} is going to be exchanged by {}".format(node_to_visit.index,key,next_node.index, new_goal_node.index))
							exchange_nodes(node_to_visit, key, next_node, new_goal_node)
						to_visit.append(next_node)
		del goal_node

	elif(mode == 'copy_graph'):
		while(len(to_visit)):
			node_to_visit = to_visit.popleft()
			node_to_visit.visited = True
			node_to_visit = copy.copy(node_to_visit)
			node_to_visit.increment_index_count()
			node_to_visit.visited = True
			for key in node_to_visit.transitions:
				for next_node in node_to_visit.transitions[key]:
					if(not next_node.visited and not next_node in to_visit):
						to_visit.append(next_node)
		


def copy_keys(from_node, to_node):
	for key in from_node.transitions:
		if(key in to_node.transitions):
			for value in from_node.transitions[key]:
				if (not value in to_node.transitions[key]):
					to_node.transitions[key].append(value)
		else:
			to_node.transitions[key] = list(from_node.transitions[key])

""" Funciton that add concats left node to right node """
def concat_operation(left, right):
	if(len(left.transitions) and (not '#' in left.transitions) and len(left.transitions) != 1):
		logical_errors.print_error(4)
	copy_keys(right, left)
	del right

""" Function that add new nodes with the union operation """
def union_operation(initial, last, new_last):
	if(len(last.transitions) and (not '#' in left.transitions) and len(left.transitions) != 1):
		logical_errors.print_error(4)
	bfs_iterative(initial, 'search_last_node', final, new_last)	

""" Function that add new nodes witht the star repetition operation"""
def star_repetition(initial, last):
	if(len(last.transitions) and (not '#' in left.transitions) and len(left.transitions) != 1):
		logical_errors.print_error(4)
	new_initial = Node()
	new_middle = Node()
	new_last = Node()
	add_transition(new_initial, new_middle, '#')
	add_transition(new_middle, new_last, '#')
	bfs_iterative(initial, 'search_last_node', last, new_middle)
	copy_keys(initial, new_middle)
	return new_initial, new_last

""" Function that add new nodes witht the positive repetition operation"""
def positive_repetition(initial, last):
	if(len(last.transitions) and (not '#' in left.transitions) and len(left.transitions) != 1):
		logical_errors.print_error(4)
	bfs_iterative(initial, 'copy_graph', None, None)
	new_star_initial, new_star_last = star_repetition(initial, last)
	concat_operation(last, new_star_initial)
	return new_star_initial, new_star_last

""" Function that adds the first node and the last 
	with the postfix transition"""
def afn_epsilon(postfix):
	for token in postfix:
		if(is_atom(token)):
			first = Node()
			last = Node()
			add_transition(first, last, token)
			stack.append(GraphStack(first, last))
		elif(token == '.'):
			second_graph = stack.pop()
			first_graph = stack.pop()
			concat_operation(first_graph.last, second_graph.initial)
			stack.append(GraphStack(first_graph.initial, second_graph.last))
		elif(token == '*'):
			graph = stack.pop()
			first, last = star_repetition(graph.initial, graph.last, True)
			del graph.initial, graph.last, graph
			stack.append(GraphStack(first, last))
		elif(token == '+'):
			graph = stack.pop()
			first, last = positive_repetition(graph.initial, graph.last)
			stack.append(GraphStack(first, last))
		elif(token == ','):
			second_graph = stack.pop()
			first_graph = stack.pop()
			bfs_iterative(second_graph.initial, 'search_last_node', second_graph.last, first_graph.last)
			copy_keys(second_graph.initial, first_graph.initial)
			del second_graph.initial, second_graph.last
			stack.append(GraphStack(first_graph.initial, first_graph.last))
	print_stack()
	del stack[:]
	global count
	count = 0



# ---------------- Functions ----------------