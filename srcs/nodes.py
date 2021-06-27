import lark
import re
from srcs.display_tree import visu_tree, print_tree
from lark import Tree, Token

def is_falsy(env, fact):
	return (fact == env.facts.enum['FALSE'] or fact == env.facts.enum['FALSE_UNSET'])

def is_true(env, fact):
	return (fact == env.facts.enum['TRUE'])

def is_undefined(env, fact):
	return (fact == env.facts.enum['UNDEFINED'])

def has_an_undefined_member(status):
	return (status % 10 == 2)

def both_are_identical(status):
	return (status % 10 == status // 10)

def at_least_a_true(status):
	return (status // 10 == 1)

def both_are_true(status):
	return (status == 11)

def at_least_a_false(status):
	return (status != 11 and status != 22 and status != 12)

# Every logical operation here are commutative, so we treat both combinations at once
def get_setting(env, left, right):
	"""
        Retrieve the current states combinations.
		2 represents an undefined state
		1 represents a true state
		0 represents a false state
    """
	if (is_true(env, left) and is_true(env, right)):
		return (11)
	elif ((is_true(env, left) and is_falsy(env, right)) or (is_true(env, right) and is_falsy(env, left))):
		return (10)
	elif ((is_true(env, left) and is_undefined(env, right)) or (is_true(env, right) and is_undefined(env, left))):
		return (12)
	elif ((is_undefined(env, left) and is_falsy(env, right)) or (is_undefined(env, right) and is_falsy(env, left))):
		return (2)
	elif (is_undefined(env, left) and is_undefined(env, right)):
		return (22)
	return (0)

# This function could be divided into multiple classes (1 per operation containing an eval method), but it feels overkill for a small project like this one
def eval_expression_recursively(env, node):
	"""
		Retrieve the state of an operation recursively, evaluating the parsing tree
	"""
	# Extract operator
	cur_node = node
	if (node.data == "operation"):
		cur_node = node.children[0]
	ope = cur_node.data
	# Handle leaf
	if (cur_node.data == "leaf"):
		leaf = cur_node.children[0]
		if (env.facts.dict[leaf] == env.facts.enum['FALSE_UNSET']):
			return (env.facts.enum['FALSE'])
		return (env.facts.dict[leaf])
	# Handle parenthesis
	elif (cur_node.data == "parenthesis"):
		new_node = cur_node.children[0]
		return (eval_expression_recursively(env, new_node))
	# Handle unary operations
	elif (cur_node.data == "unary"):
		new_node = cur_node.children[0]
		ret_tmp = eval_expression_recursively(env, new_node)
		if (is_true(env, ret_tmp)):
			return (env.facts.enum['FALSE'])
		elif (is_undefined(env, ret_tmp)):
			return (env.facts.enum['UNDEFINED'])
		return (env.facts.enum['TRUE'])
	# Handle binary operations
	left_node = cur_node.children[0]
	right_node = cur_node.children[2]
	left_ret = eval_expression_recursively(env, left_node)
	right_ret = eval_expression_recursively(env, right_node)
	setting = get_setting(env, left_ret, right_ret)
	# Handle xor
	if (cur_node.data == "xor"):
		if (has_an_undefined_member(setting)):
			return env.facts.enum['UNDEFINED']
		elif (both_are_identical(setting)):
			return env.facts.enum['FALSE']
		return env.facts.enum['TRUE']
	# Handle and
	elif (cur_node.data == "and"):
		if (at_least_a_false(setting)):
			return env.facts.enum['FALSE']
		elif (has_an_undefined_member(setting)):
			return env.facts.enum['UNDEFINED']
		return env.facts.enum['TRUE']
	# Handle or
	if (at_least_a_true(setting)):
		return env.facts.enum['TRUE']
	elif (has_an_undefined_member(setting)):
		return env.facts.enum['UNDEFINED']
	return env.facts.enum['FALSE']

all_paths = []

def get_tree_path(env, fact, node, dt = []):
	"""
		Get all paths for a given fact within the parsing tree
	"""
	# Extract operator
	cur_node = node
	if (node.data == "operation"):
		cur_node = node.children[0]
	# Handle leaf
	if (cur_node.data == "leaf"):
		leaf = cur_node.children[0]
		if (leaf == fact):
			dt += leaf
			all_paths.append(dt)
	ope_type = cur_node.data
	# Handle unary & parenthesis
	if (ope_type == "unary" or ope_type == "parenthesis"):
		new_node = cur_node.children[0]
		get_tree_path(env, fact, new_node, dt + [ope_type])
	# Handle binary
	elif (ope_type != "leaf"):
		left_node = cur_node.children[0]
		right_node = cur_node.children[2]
		left_path = get_tree_path(env, fact, left_node, dt + [ope_type])
		right_path = get_tree_path(env, fact, right_node, dt + [ope_type])

def factorise_states(env, states):
	"""
		Factorise the resulting states to an unique global state
	"""
	nb_false = 0
	nb_true = 0
	for i in range(len(states)):
		if (is_true(env, states[i])):
			nb_true += 1
		elif (is_falsy(env, states[i])):
			nb_false += 1
	if (nb_false > 0 and nb_true == 0):
		return (env.facts.enum['FALSE'])
	elif (nb_true > 0):# and nb_false == 0):
		return (env.facts.enum['TRUE'])
	return (env.facts.enum['UNDEFINED'])

def extract_state(env):
	"""
		Convert paths to states and factorise them to retrieve the global state
	"""
	states = []
	# Convert path to states conv
	for i in range(len(all_paths)):
		curr_path = all_paths[i]
		curr_state = env.facts.enum['TRUE']
		for j in range(len(curr_path)):
			if (curr_path[j] == "unary"):
				if (is_true(env, curr_state)):
					curr_state = env.facts.enum['FALSE']
				elif (is_falsy(env, curr_state)):
					curr_state = env.facts.enum['TRUE']
			elif (curr_path[j] == "xor" or curr_path[j] == "or"):
				curr_state = env.facts.enum['UNDEFINED']
		states.append(curr_state)
	# Get the final (global) state conv for the given fact
	return (factorise_states(env, states))

def apply_boolean(env, lhs, rhs):
	if (lhs == env.facts.enum['UNDEFINED'] or rhs == env.facts.enum['UNDEFINED']):
		return (env.facts.enum['UNDEFINED'])
	elif (is_true(env, lhs)):
		if (is_true(env, rhs)):
			return (env.facts.enum['TRUE'])
		return (env.facts.enum['FALSE'])
	else:
		if (is_true(env, rhs)):
			return (env.facts.enum['FALSE'])
	return (env.facts.enum['TRUE'])

#def apply_fact(env, fact, state):
#	current_fact_state = env.facts.dict[fact]


def establish_if_not_established(env, fact_curr):
	if (env.facts.dict[fact_curr] == env.facts.enum['FALSE_UNSET']):
		states_list = []
		ruleset = env.adj_matrix.loc[fact_curr, :]
		ruleset_pruned = ruleset[ruleset != 0]
		if (ruleset_pruned.size == 0):
			env.facts.dict[fact_curr] = env.facts.enum['FALSE']
		else:
			for index, value in ruleset_pruned.items():
				states_list.append(eval_tree(env, index, fact_curr))
			#print(states_list)
			factorised = factorise_states(env, states_list)
			#print(factorised)
			env.facts.dict[fact_curr] = factorised

### Todo : "<=>" operator
def eval_tree(env, rule, fact, two_sided = False):
	# Establish the state for every unset states within the facts dict
	facts_list = re.findall(r'[A-Z]', re.split(r'=>', rule)[0])
	for fact_curr in facts_list:
		establish_if_not_established(env, fact_curr)
	# Tree traversal, get left and right composents
	tree = env.rules.dict[rule]
	sign = tree.children[1]
	left_result = eval_expression_recursively(env, tree.children[0])
	if (two_sided == True):
		right_result = eval_expression_recursively(env, tree.children[2])
	# Right paths
	all_paths.clear()
	get_tree_path(env, fact, tree.children[2])
	state = extract_state(env)
	# Apply right to left
	final_right_state = apply_boolean(env, left_result, state)

	# Return final state
	return (final_right_state)

def create_rules_trees(params, env):
    ### Pour acceder a la mémoire de l'arbre
    ### https://lark-parser.readthedocs.io/en/latest/classes.html#tree

    grammar = """
        start: operation ARROW operation
        leaf: LETTER
        parenthesis.-2: "(" operation ")"
        unary.-1: "!" operation
        and.4: operation AND operation
        or.5: operation OR operation
        xor.6: operation XOR operation
        operation: parenthesis
            | unary
            | and
            | xor
            | leaf
            | or

        OR: ("|")
        XOR: ("^")
        AND: ("+")
        ARROW: /(=>|<=>)+/
        LETTER: /[A-Z]+/
        %ignore " "
    """
    p = lark.Lark(grammar, priority='decay')
    for element in env.adj_matrix.columns.values:
        env.rules.dict[element] = p.parse(element)
        if params.visual:
            print_tree(env.rules.dict[element]) ## Print the rules's tree in terminal
        if params.display:
            visu_tree(env.rules.dict[element]) ## Display the rule's tree
        print(element)

    for q in env.queries:
        establish_if_not_established(env, q)
        print(q + " : " + env.facts.dict[q].name)
    print(env.facts.dict)
        #eval_tree(env, element, 'A')


	# print(env.adj_matrix)
    ## print(env.rules.dict)
    # print(env.rules.dict['A+B=>C'].children[0])
    # print(env.facts.dict)
    # print(env.facts.dict['F'] == env.facts.enum['FALSE'])
