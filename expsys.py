from srcs.parsing import parse_args, parse_input
from srcs.data_struct import Setup, Facts, Rules, Env
from srcs.const import *
from srcs.execute import execute_queries

import pandas as pd




def main():
    args = parse_args()

    params = Setup(args.modify, args.visual, args.display_trees, args.input_file, args.verbose)
    adj_matrix = pd.DataFrame(index=ALL_FACTS) # matrix indexes pre-set so we juste have to add columns by columns (rules)
    facts = Facts()
    rules = Rules()
    env = Env(facts, rules, adj_matrix)
    env.verbose = params.verbose

    first_iter = True
    while params.modify or first_iter:
        parse_input(params, env, first_iter)
        first_iter = False
        execute_queries(env)

        if params.modify:
            print(SAKURA, "\nDo you want to modify inputs ? [yes / no]", DEFAULT)
            input_ = input()
            if input_ == "no":
                break



if __name__ == "__main__":
    main()