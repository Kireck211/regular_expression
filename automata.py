from collections import deque
from sys import argv

operator_priority = [["(", ")"],["*"], ["+"], [".", ","]];
deque = deque([])
stack = []
script, file_name = argv

def return_priority(operator):
	for index, operators in enumerate(operator_priority):
		if operator in operators:
			return index
	return -1

def add_concats(regular_expression):
	new_regular_expression = []
	for i in range(0, len(regular_expression) - 1):
		new_regular_expression.append(regular_expression[i])
		if (regular_expression[i].isalpha() and regular_expression[i+1].isalpha()):
			new_regular_expression.append(".")
		elif (regular_expression[i].isalpha() and regular_expression[i+1] == "("):
			new_regular_expression.append(".")
		elif (return_priority(regular_expression[i]) > 0 and regular_expression[i+1].isalpha()):
			new_regular_expression.append(".")
		elif (return_priority(regular_expression[i]) == 0 and regular_expression[i+1].isalpha()):
			new_regular_expression.append(".")
		elif ((return_priority(regular_expression[i]) < 0 and not regular_expression[i].isalpha()) and return_priority(regular_expression[i]) < 0):
			new_regular_expression.append(".")

	new_regular_expression.append(regular_expression[len(regular_expression)-1])
	return "".join(new_regular_expression)

def shunting_yard(regular_expression, deque, stack):
	for token in regular_expression:
		token = Token(token)
		if token.priority == -1:
			deque.append(token)
		elif token.priority == 1:
			if token.value == "(":
				stack.append(token)
			else:
				last = stack.pop()
				while(last.value != "("):
					deque.append(last)
					last = stack.pop()
		else:
			while (len(stack) != 0):
				if (token.priority <= stack[len(stack)-1].priority):
					deque.append(stack.pop())
				else:
					break
			stack.append(token)
	while len(stack) != 0:
		deque.append(stack.pop())



class Token(object):
	"""Creates a token object"""
	def __init__(self, token):
		self.value = token
		self.priority = return_priority(token)

input_file = open(file_name)
regular_expression = input_file.readline()
regular_expression = add_concats(regular_expression)
print(regular_expression)

shunting_yard(regular_expression, deque, stack)
print("Printing stack:")
for element in stack:
	print(element.value)
print("Printing deque:")
for element in deque:
	print(element.value, end=" ")
