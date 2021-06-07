import lark
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

def eval_expression_recursively(env, node):
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

def eval_tree(env, rule):
	tree = env.rules.dict[rule]
	sign = tree.children[1]
	left_result = eval_expression_recursively(env, tree.children[0])
	right_result = eval_expression_recursively(env, tree.children[2])
	print(left_result)
	print(right_result)

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
        eval_tree(env, element)
    # print(env.adj_matrix)
    ## print(env.rules.dict)
    # print(env.rules.dict['A+B=>C'].children[0])
    # print(env.facts.dict)
    # print(env.facts.dict['F'] == env.facts.enum['FALSE'])
