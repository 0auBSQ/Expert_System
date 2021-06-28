from srcs.eval import *
from srcs.const import *

def execute_queries(env):
	try:
		print(GREEN,"\n === EXECUTION ===", DEFAULT,"\n")
		for q in env.queries:
			establish_if_not_established(env, q)
		print("")
		for q in env.queries:
			color = retrieve_color_seq(env, env.facts.dict[q])
			print(q + " : " + color + env.facts.dict[q].name + DEFAULT)
		print(GREEN,"\n ====== END ======", DEFAULT,"\n")
	except RecursionError:
		print("\nHmm... :", SAKURA, "Looks like your execution is stuck into a loop, try expliciting some facts.", DEFAULT,"\n")
