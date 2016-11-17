from collections import deque

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

""" Class used to show logical errors and exit the program """
class Errors(object):
	"""Creates an object with all the posibles bugs"""
	def __init__(self):
		self.errors = [
			'A postfix has a \"(\" or \")\"', 
			'Postfix was not well build, trying to pop of empty stack', 
			'Cannot remove key_transition, because transition is not in the left_node',
			'This final node has transitions'
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

def print_graph(node):
	print("The node {} has the next transitions: ".format(node.index))
	for key in node.transitions:
		print(key+': ', end="")
		for value in node.transitions[key]:
			print(str(value.index), end=" ")
	print("")

""" Function that prints all the graph and its transitions"""
def print_stack():
	print("The length of the stack: " + str(len(stack)))
	for graph in stack:
		print_graph(graph.initial)


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

""" Funciton that add concats left node to right node """
def concat_operation(left, right):
	if(len(left.transitions) and (not '#' in left.transitions) and len(left.transitions) != 1):
		logical_errors.print_error(4)
	left.transitions = right.transitions.copy()
	del right


""" Function that add new nodes with the union operation """
def union_operation():
	return True

""" Function that add new nodes witht the star repetition operation"""
def star_repetition(first, last):
	if(len(last.transitions)):
		logical_errors.print_error(4)
	new_first = Node()
	new_last = Node()
	add_transition(new_first, first, '#')
	add_transition(last, new_last, '#')
	add_transition(new_first, new_last, '#')
	add_transition(new_last, first, '#')
	return new_first, new_last


""" Function that add new nodes witht the positive repetition operation"""
def positive_repetition():
	return True
		

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
			second = stack.pop()
			first = stack.pop()
			concat_operation(first.last, second.initial)
			stack.append(GraphStack(first.initial, second.last))
		elif(token == '*'):
			graph = stack.pop()
			first, last = star_repetition(graph.initial, graph.last)
			stack.append(GraphStack(first, last))


# ---------------- Functions ----------------