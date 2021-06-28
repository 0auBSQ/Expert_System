import re
from srcs.const import *
from srcs.state_transform import *
from srcs.state_operations import *

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

def establish_if_not_established(env, fact_curr, children = False):
	"""
		Determine recursively the necessary facts
	"""
	if (env.facts.dict[fact_curr] == env.facts.enum['FALSE_UNSET']):
		if (env.verbose == True and children == True):
			print(GRAY + "CHECK > '" +  YELLOW + fact_curr + GRAY + "' is asked but unset, retrieving in process..." + DEFAULT)
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
	# Verbose
	if (env.verbose == True):
		print("Searching '" + YELLOW + fact + DEFAULT + "' using the rule '" + BLUE + rule + DEFAULT + "'...")
	# Establish the state for every unset states within the facts dict
	facts_list = re.findall(r'[A-Z]', re.split(r'=>', rule)[0])
	for fact_curr in facts_list:
		establish_if_not_established(env, fact_curr, True)
	# Tree traversal, get left and right composents
	tree = env.rules.dict[rule]
	sign = tree.children[1]
	left_result = eval_expression_recursively(env, tree.children[0])
	#if (two_sided == True):
	#	right_result = eval_expression_recursively(env, tree.children[2])
	# Right paths
	all_paths.clear()
	get_tree_path(env, fact, tree.children[2])
	state = extract_state(env, all_paths)
	# Apply right to left
	final_right_state = apply_boolean(env, left_result, state)

	# Additional verbose
	if (env.verbose == True):
		print(GRAY + "EVAL > LHS is " + retrieve_color_seq(env, left_result) + left_result.name + GRAY + " in '" + BLUE + rule + GRAY + "'." + DEFAULT)
		print(GRAY + "EVAL > RHS factor is " + retrieve_color_seq(env, state) + state.name + GRAY + " in '" + BLUE + rule + GRAY + "'." + DEFAULT)
		print("'" + YELLOW + fact + DEFAULT + "' is established to " + retrieve_color_seq(env, final_right_state) + final_right_state.name + DEFAULT + " using the rule '" + BLUE + rule + DEFAULT + "'.")

	# Return final state
	return (final_right_state)
