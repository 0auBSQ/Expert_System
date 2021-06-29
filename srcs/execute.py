from srcs.eval import *
from srcs.const import *


uncertain = []


def execute_queries(env):
	"""
		Execute the backward chaining engine using the env configuration.
		Only edits the facts dictionnary.
		If infinite loop an error is triggered without quitting the program.
	"""
	try:
		print(GREEN,"\n === EXECUTION ===", DEFAULT,"\n")
		uncertain.clear()
		for q in env.queries:
			if (q in uncertain):
				env.facts.dict[q] = env.facts.enum['FALSE_UNSET']
			establish_if_not_established(env, q, uncertain)
		print("")
		for q in env.queries:
			color = retrieve_color_seq(env, env.facts.dict[q])
			print(q + " : " + color + env.facts.dict[q].name + DEFAULT)
		if (len(uncertain) > 0):
			print("\nUncertain : " + RED + ' '.join(uncertain) + DEFAULT)
			print(GRAY + "NOTE > Uncertain facts are caused by loop errors, they might cause resolving issues" + DEFAULT)
		print(GREEN,"\n ====== END ======", DEFAULT,"\n")
	except RecursionError:
		print("\nHmm... :", SAKURA, "Looks like your execution is stuck into a loop, try expliciting some facts.", DEFAULT,"\n")
