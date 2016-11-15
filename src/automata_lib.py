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
		index = len(graph)
		self.index = index
		self.transitions = {}
		self.initial = False
		self.final = False
		graph.append(self)

""" Class used to show logical errors and exit the program """
class Errors(object):
	"""Creates an object with all the posibles bugs"""
	def __init__(self):
		self.errors = [
			'A postfix has a \"(\" or \")\"', 
			'Postfix was not well build, trying to pop of empty stack', 
			'Cannot remove key_transition, because transition is not in the left_node'
		]

	def error(index):
		print(self.errors[index])
		exit(index)

class NodeTransition(object):
	""" Creates an object to add to the queue and execute operation """
	def __init__(self, node, transition):
		self.node = node
		self.transition = transition

# ---------------- Classes ----------------




# ---------------- Global variables  ----------------

# Global priority operators indexes
operator_priority = [["(", ")"],["*","+"], [".", ","]];

# Global graph variable
graph = []

# Global errors object
logical_errors = Errors()

# Global queue of not atoms
queue = deque([])

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
	if (len(characters) == 1 and return_priority(characters) < 0):
		return True
	return False


""" Function that prints all the graph and its transitions"""
def print_graph():
	for node in graph:
		if (len(node.transitions)):
			print("The state {} has the following transitions:".format(node.index))
			for key in node.transitions:
				for pointed_node in node.transitions[key]:
					print("\"{}\" : {}".format(key, pointed_node.index))
		else:
			print("The state {} has no transitions".format(node.index))
		print("")

""" Function that prints the lenght of the queue,
	keys and value in that key"""
def print_queue():
	print("The queue has {} nodes to check".format(len(queue)))
	for node in queue:
		print("The node {} has {} transition".format(node.node.index, node.transition))

def is_node_queue(node, key_transition):
	if (not len(queue)):
		return False
	print(node in queue)
	#print(node.node.transition + " " + key_transition)
	#print(node.transition == key_transition)
	if (node in queue and node.transition == key_transition):
		return True
	return False

""" Function that appends to the general queue transitions to check"""
def append_not_atom(node, key_transition):
	# The key_transition has possibilities to append
	if (not is_atom(key_transition)):
		print("Entered because is not an atom")

		# The key don't exist in the queue
		if (not is_node_queue(node, key_transition)):
			#print("Entered because the queue hasn't this {} as key".format(node.index))
			node_transition = NodeTransition(node, key_transition)
			queue.append(node_transition)
			return True
	
	# The key_transition not appended, return False
	return False


""" Function that adds a transition from the left_node 
	to the right_node with the transition 
	of key_transition"""
def add_transition(left_node, right_node, key_transition):
	append_not_atom(left_node, key_transition)
	if (not key_transition in left_node.transitions):
		left_node.transitions[key_transition] = []
	left_node.transitions[key_transition].append(right_node)


""" Function that removes transition with the value 
	of key_transition from left_node 
	to right_node"""
def remove_transition(left_node, right_node, key_transition):
	if (not key_transition in left_node.transitions):
		logical_errors(3)
	left_node.transitions[key_transition].remove(right_node)


""" Funciton that add new nodes with concat operation """
def concat_operation(left_node, right_node, postfix):
	node = Node()
	new_postfix = postfix.replace(".","", 1)
	add_transition(node, right_node, new_postfix[1:])
	add_transition(left_node, node, postfix[0])
	remove_transition(left_node, right_node, postfix)

""" Function that add new nodes with the union operation """
def union_operation():
	return True

""" Function that add new nodes witht the star repetition operation"""
def star_repetition():
	return True

""" Function that add new nodes witht the positive repetition operation"""
def positive_repetition():
	return True

""" Function that creates a node between 
	nodes with a not atom transition"""
def add_node():
	while(len(queue)):
		next = queue[0]
		print(next)
		#print_queue()
	#while(len(queue)):
		

""" Function that adds the first node and the last 
	with the postfix transition"""
def initialize_graph(postfix):
	initial = Node()
	final = Node()
	initial.initial = True
	add_transition(initial,final,postfix)
	append_not_atom(initial, postfix)
	#add_node()


# ---------------- Functions ----------------