from srcs.parsing import parse_args, parse_input
from srcs.data_struct import Setup, Facts, Rules, Env
from srcs.const import *

import pandas as pd




def main():
    args = parse_args()

    params = Setup(args.modify, args.visual, args.input_file)
    adj_matrix = pd.DataFrame(index=ALL_FACTS) # matrix indexes pre-set so we juste have to add columns by columns (rules)
    facts = Facts()
    rules = Rules()
    env = Env(facts, rules, adj_matrix)
    
    parse_input(params, env)



if __name__ == "__main__":
    main()