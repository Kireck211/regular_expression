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
		global graph
		self.index = len(graph)
		self.transitions = {}
		self.initial = False
		self.final = False
		graph.append(self)

""" Class used to show logical errors and exit the program """
class Errors(object):
	"""Creates an object with all the posibles bugs"""
	def __init__(self):
		self.errors = ['A postfix has a \"(\" or \")\"', 'Postfix was not well build, trying to pop of empty stack']

	def error(index):
		print(self.errors[index])
		exit(index)

# ---------------- Classes ----------------

# ---------------- Global variables  ----------------

# Global priority operators indexes
operator_priority = [["(", ")"],["*","+"], [".", ","]];

# Global graph variable
graph = []

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

""" Function that returns true if an array of chars
	is a regular expression or false if it is 
	a valid node creation rule"""
def is_regular_expression(characters):
	return False

""" Function that creates new nodes between left_node and
	right_node with their transitions according to the
	characters"""
def add_node(token, stack, left_node, right_node):
	# if priority == 1 means it it * or +
	if (is_regular_expression(characters)):
		regex = characters.join('')
		left_node.transitions[regex] = []
		left_node.transitions[regex].append(right_node)

	if (priority == 1):
		if (characters[0] == '*'):
			inter_node = Node(len(graph) - 1)
			left_node.transitions['#'] = inter_node
			inter_node.transitions['#'] = right_node
			inter_node.transitions[characters[1]] = inter_node
		elif (characters[0] == '+'):
			inter_node = Node(len(graph) - 1)
			second_inter_node = Node(len(graph) - 1)
			left_node.transitions[characters[1]].append(inter_node)
			inter_node.transitions['#'] = []
			inter_node.transitions['#'].append(right_node)
			inter_node.transitions[characters[1]] = []
			inter_node.transitions[characters[1]].append(inter_node)
	elif (priority == 2):
		return 0

	else: 
		logical_errors.error(1)

def initialize_graph(postfix):
	initial = Node()
	final = Node()
	initial.initial = True
	initial.transitions[postfix] = []
	initial.transitions[postfix].append(final)

# ---------------- Functions ----------------