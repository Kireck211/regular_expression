from collections import *
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
		self.index = count
		count += 1

	def get_count(self):
		global count
		return count

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

CONST_CONCAT = ":"
CONST_OR = ","
CONST_PLUS = "+"
CONST_STAR = "*"

# Global priority operators indexes
operator_priority = [["(", ")"],[CONST_STAR,CONST_PLUS], [CONST_OR], [CONST_CONCAT]];

# Global stack variable
stack = []

# Global counter of nodes
count = 0

# Global errors object
logical_errors = Errors()

# Global list of nodes
node_list = []

# Global afn
complete_afn = []

# Global list of actual nodes
actual_nodes = []

# Global accepted string
accepted_string = ""

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
		if(regular_expression[i] == '\\' and return_priority(regular_expression[i]) < 0):
			a = 1
		if (regular_expression[i].isalpha()):
			if(regular_expression[i+1].isalpha()):
				new_regular_expression.append(CONST_CONCAT)
			elif(return_priority(regular_expression[i+1]) < 0):
				new_regular_expression.append(CONST_CONCAT)
			elif(regular_expression[i+1] == '('):
				new_regular_expression.append(CONST_CONCAT)
		elif (regular_expression[i] == ')'):
			if (regular_expression[i+1] == '('):
				new_regular_expression.append(CONST_CONCAT)
			elif(return_priority(regular_expression[i+1]) < 0):
				new_regular_expression.append(CONST_CONCAT)
		elif (return_priority(regular_expression[i]) > 0 and return_priority(regular_expression[i]) < 2):
			if (regular_expression[i+1].isalpha()):
				new_regular_expression.append(CONST_CONCAT)
			if (regular_expression[i+1] == '('):
				new_regular_expression.append(CONST_CONCAT)
		elif (return_priority(regular_expression[i]) < 0):
			if(return_priority(regular_expression[i+1]) < 0):
				new_regular_expression.append(CONST_CONCAT)

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
			while(len(stack) and stack[len(stack)-1].priority >= token.priority and stack[len(stack) - 1].value != '('): 
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
	#print("The length of the stack: " + str(len(stack)))
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
			print("The node {} has the next transitions:".format(node_to_visit.index), end="")
			if (node_to_visit.initial):
				print(" (initial node)", end="")
			if (node_to_visit.final):
				print(" (final node)", end="")
			print("")
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
		bfs_iterative(node, 'clear_visited', None, None)

	elif(mode == 'change_indexes'):
		consecutive = 0
		while(len(to_visit)):
			node_to_visit = to_visit.popleft()
			if (consecutive != node_to_visit.index):
				node_to_visit.index = consecutive
			consecutive += 1
			node_to_visit.visited = True
			for key in node_to_visit.transitions:
				for next_node in node_to_visit.transitions[key]:
					if(not next_node.visited and not next_node in to_visit):
						to_visit.append(next_node)
		bfs_iterative(node, 'clear_visited', None, None)

	elif(mode == 'create_node_list'):
		new_node_list = []
		while(len(to_visit)):
			node_to_visit = to_visit.popleft()
			new_node_list.append(node_to_visit)
			node_to_visit.visited = True
			for key in node_to_visit.transitions:
				for next_node in node_to_visit.transitions[key]:
					if(not next_node.visited and not next_node in to_visit):
						to_visit.append(next_node)
		bfs_iterative(node, 'clear_visited', None, None)
		return sorted(list(set(new_node_list)), key=get_index)

def print_transitions(list_of_nodes):
	for node in list_of_nodes:
		print("index: {}, transitions: {}".format(node.index, node, node.transitions))

def get_index(node):
	return node.index

def copy_node(node):
	node_copied = Node()
	for key in node.transitions:
		node_copied.transitions[key] = copy.copy(node.transitions[key])
	node_copied.increment_index_count()
	return node_copied
		
def copy_graph(initial, last):
	copy_initial = copy_node(initial)
	copies_factory = {initial.index: copy_initial}
	to_visit = deque([copy_initial])
	while(len(to_visit)):
		node = to_visit.popleft()
		node.visited = True
		for key in node.transitions:
			for next_node in node.transitions[key]:
				if (not next_node.index in copies_factory):
					copies_factory[next_node.index] = copy_node(next_node)
				exchange_nodes(node, key, next_node, copies_factory[next_node.index])
				if(not copies_factory[next_node.index].visited and not copies_factory[next_node.index] in to_visit):
					to_visit.append(copies_factory[next_node.index])
	bfs_iterative(copies_factory[initial.index], 'clear_visited', None, None)
	return copies_factory[initial.index], copies_factory[last.index]

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
	#bfs_iterative(initial, 'copy_graph', None, None)
	new_star_initial, new_star_last = copy_graph(initial, last)
	new_star_initial, new_star_last = star_repetition(new_star_initial, new_star_last)
	concat_operation(last, new_star_initial)
	return initial, new_star_last

""" Function that adds the first node and the last 
	with the postfix transition"""
def afn_epsilon(postfix):
	for token in postfix:
		if(is_atom(token)):
			first = Node()
			last = Node()
			add_transition(first, last, token)
			stack.append(GraphStack(first, last))
		elif(token == CONST_CONCAT):
			second_graph = stack.pop()
			first_graph = stack.pop()
			concat_operation(first_graph.last, second_graph.initial)
			stack.append(GraphStack(first_graph.initial, second_graph.last))
		elif(token == CONST_STAR):
			graph = stack.pop()
			first, last = star_repetition(graph.initial, graph.last)
			del graph.initial, graph.last, graph
			stack.append(GraphStack(first, last))
		elif(token == CONST_PLUS):
			graph = stack.pop()
			first, last = positive_repetition(graph.initial, graph.last)
			stack.append(GraphStack(first, last))
		elif(token == CONST_OR):
			second_graph = stack.pop()
			first_graph = stack.pop()
			bfs_iterative(second_graph.initial, 'search_last_node', second_graph.last, first_graph.last)
			copy_keys(second_graph.initial, first_graph.initial)
			del second_graph.initial, second_graph.last
			stack.append(GraphStack(first_graph.initial, first_graph.last))
	bfs_iterative(stack[0].initial, 'change_indexes', None, None)
	global node_list
	del node_list[:]
	node_list = bfs_iterative(stack[0].initial, 'create_node_list', None, None)
	node_list[stack[0].initial.index].initial = True
	node_list[stack[0].last.index].final = True

def epsilon_closure(initial_node):
	reachable_nodes = [initial_node]
	to_visit = deque([initial_node])
	while(len(to_visit)):
		node = to_visit.popleft()
		node.visited = True
		if ('#' in node.transitions):
			for node_to_visit in node.transitions['#']:
				if (not node_to_visit.visited and not node_to_visit in to_visit):
					to_visit.append(node_to_visit)
					if(not node_to_visit in reachable_nodes):
						reachable_nodes.append(node_to_visit)
	bfs_iterative(initial_node, 'clear_visited', None, None)
	return reachable_nodes

def get_alphabet(initial_node):
	alphabet = []
	to_visit = deque([initial_node])
	while(len(to_visit)):
		node = to_visit.popleft()
		node.visited = True
		for key in node.transitions:
			if (not key in alphabet and key != '#'):
				alphabet.append(key)
			for node_to_visit in node.transitions[key]:
				if (not node_to_visit.visited and not node_to_visit in to_visit):
					to_visit.append(node_to_visit)
	bfs_iterative(initial_node, 'clear_visited', None, None)
	return alphabet

def remove_copies(list_of_nodes):
	new_list = []
	for elements in list_of_nodes:
		if (isinstance(elements, Iterable)):
			for element in elements:
				new_list.append(element)
		else:
			new_list.append(elements)
	return list(set(new_list))

def create_afn(second_column):
	afn = []
	for i in range(0, len(second_column)):
		afn.append(Node())
		if(i == 0):
			afn[i].initial = True
		if(node_list[i].final):
			afn[i].final = True
	for index in second_column:
		for letter in second_column[index]:
			for node in second_column[index][letter]:
				add_transition(afn[index], afn[node.index], letter)
	bfs_iterative(afn[0], 'change_indexes', None, None)
	return afn

def afn():
	first_column = []
	alphabet = get_alphabet(node_list[0])
	for node in node_list:
		first_column.append(epsilon_closure(node))
	index = 0
	for nodes in first_column:
		for node in nodes:
			if (len(node.transitions) == 0):
				node_list[index].final = True
		index += 1
	second_column = {}
	index = 0
	for list_of_nodes in first_column:
		second_column[index] = {}
		for letter in alphabet:
			for node in list_of_nodes:
				if (letter in node.transitions):
					if(letter in second_column[index]):
						for n_node in node.transitions[letter]:
							second_column[index][letter].append(n_node)
					else:
						second_column[index][letter] = copy.copy(node.transitions[letter])
		index += 1
	for index in second_column:
		for letter in second_column[index]:
			for node in second_column[index][letter]:
				epsilon_list = epsilon_closure(node)
				for epsilon_node in epsilon_list:
					if(not epsilon_node in second_column[index][letter]):
						second_column[index][letter].append(epsilon_node)
	afn = create_afn(second_column)
	bfs_iterative(afn[0], 'print', None, None)
	global complete_afn
	global actual_nodes
	complete_afn = afn[0]
	actual_nodes.append(complete_afn)

def convertInput(text):
	text = "\\n".join(text.split("\r\n"))
	text = text.replace(" ", "_")
	return text

def inFinalState():
	for node in actual_nodes:
		if(node.final):
			return True
	return False

def consume(character):
	global actual_nodes
	global accepted_string
	atLeastOne = False
	printed = False
	for node in actual_nodes:
		if (character in node.transitions):
			atLeastOne = True
			for next_node in node.transitions[character]:
				if (not next_node in actual_nodes):
					actual_nodes.append(next_node)
			if(inFinalState()):
				if(not printed):
					accepted_string += character
					print(accepted_string)
					printed = True
	if(not atLeastOne):
		del actual_nodes[:]
		actual_nodes.append(complete_afn)
		accepted_string = ""

# ---------------- Functions ----------------