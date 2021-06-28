from srcs.state_operations import *
from srcs.const import *

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

def extract_state(env, all_paths):
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

def retrieve_color_seq(env, state):
	if (is_falsy(env, state)):
		return RED
	elif (is_true(env, state)):
		return GREEN
	return GRAY
