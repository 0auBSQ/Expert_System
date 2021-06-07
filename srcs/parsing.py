import argparse
import pandas as pd
import sys
import re
import copy

from srcs.const import *
from srcs.nodes import *

def parse_args():

    parser = argparse.ArgumentParser(description="expert-system")
    parser.add_argument("input_file", help="File with sets of rules, facts and queries (optional). If not given the program read on STDIN", nargs='?')
    parser.add_argument("--modify", "-m", help="add the possibility to modify the state of a fact at the end of the process", action="store_true")
    parser.add_argument("--visual", "-v", help="shell visualisation of the rule's trees", action="store_true")
    parser.add_argument("--display_trees", "-d", help="Diplay each rule's trees", action="store_true")
    args = parser.parse_args()

    return args

def add_facts(facts, line):
    """
        Iterate over the line, skip the first character and check if there is a '!', in this case the fact will be set or re-set as FALSE
        in the orther case facts will be TRUE
        <$ added : define a fact as FALSE_UNSET>
    """
    i = 1
    length = len(line)
    while i < length:
        if line[i] == '!':
            facts.dict[line[i+1]] = facts.enum['FALSE']
            i += 2
        elif line[i] == '$':
            facts.dict[line[i+1]] = facts.enum['FALSE_UNSET']
            i += 2
        else :
            facts.dict[line[i]] = facts.enum['TRUE']
            i += 1


def add_queries(query_tab, line):
    """
        Iterate over the line and depend of if there is a '!' in front of the char:
            case '![A-Z]' : If the query is in the query_tab, remove it
            case '[A-Z]' : If the query is not in the query_tab, append it
    """
    i = 1
    length = len(line)

    while i < length:
        if line[i] == '!':
            if line[i+1] in query_tab:
                query_tab.remove(line[i+1])
            i += 2
        else :
            if line[i] not in query_tab:
                query_tab.append(line[i])
            i += 1

def add_rules_in_matrix(matrix, line):
    """
        Add a column in the matrix called by the value of 'line'
        and set 0 or 1 in the column depend if the fact is present or not in the 'line'
    """
    if re.match('^.*<=>.*$', line):
        facts_list = re.findall(r'[A-Z]', line) ### Store all A-Z in a list to iter on it
    else:
        facts_list = re.findall(r'[A-Z]', re.split(r'=>', line)[1])
    matrix[line] = 0
    # facts_list = re.findall(r'[A-Z]', line) ### Store all A-Z in a list to iter on it
    for fact in facts_list:
        matrix[line].loc[fact] = 1

def check_parenthese(token):
    """
        Check if there is the same number of '(' and ')' in a token and make sure there is no opened parenthese left.
        params :
            token : string
        return :
            Bool (True if token valid)
    """
    i = 0
    for elem in token:
        if elem == '(':
            i += 1
        elif elem == ')':
            i -= 1
        if i < 0:
            return False
    if i == 0:
        return True
    else:
        return False

def check_left_right_rules(line):
    splitted = re.split(r'=>|<=>', line) ## cut the line in two part

    ### Check number of implies (only one accepted)
    if len(splitted) != 2:
        return line, "A rule can only implie once"

    ### Check parsing for each side
    ###  re.match(r'^(\(*!?[A-Z]\)*)([\+\|\^]\(*!?[A-Z]\)*)*$'
    if re.match(r'^((!?\()*!?[A-Z]\)*)([\+\|\^](!?\()*!?[A-Z]\)*)*$', splitted[0]) is None:
        return splitted[0], "Left Token is Bad"
    if re.match(r'^(\(*!?[A-Z]\)*)([\+\|\^]\(*!?[A-Z]\)*)*$', splitted[1]) is None:
        return splitted[1], "Right Token is Bad"

    ### Check parentheses for each side
    if check_parenthese(splitted[0]) is False:
        return splitted[0], "Left Token parentheses does not match"
    if check_parenthese(splitted[1]) is False:
        return splitted[1], "Right Token parentheses does not match"

    return None, None



def parse_line(env, line):
    """
        Main function to parse a line. Depends on the case it will deal with the line as a rule, fact or query.
        There is no importance about the orders in which they are given
        params :
            env : class Env()
            line : string (represent a line of the input)
    """

    # Remove useless part of the string, white spaces and new lines
    line = line.split("#")[0].replace(" ", "").replace("\n", "")

    # Check if the line is good with regex
    if re.match(r'.*(=>|<=>)', line): ## Rules case
        token, err = check_left_right_rules(line)
        if err is not None:
            print("\n", err, " : ", RED, token, DEFAULT,"\n")
            sys.exit()
        add_rules_in_matrix(env.adj_matrix, line)

    elif re.match(r'^[=]([!]?[A-Z])*$', line): ## Fact case
        add_facts(env.facts, line) # Set given facts as true (accept more than one line of initial facts)

    elif re.match(r'^[?]([!]?[A-Z])*$', line): ## Query case
        add_queries(env.queries, line) # add the new Queries in the query tab in env

    elif line == "":
        pass

    else:
        print("\nBad line : ", RED, line, DEFAULT,"\n")
        sys.exit()

def parse_file(params, env):
    """
        This func will parse Fact, rules and Queries in case the user choose to give a file as input
        params :
            params  : Setup obj
            Env     : Env obj
        return :
            Nothing
    """

    # If the path is good, open file and store it in file_, if the file doesnt exist : return an error
    try: file_ = open(params.file, "r")
    except: print("\nFile :  [", RED, params.file, DEFAULT, "]  ==> does not exist\n"); sys.exit()

    # read the file line by line and send the line to a parsing function which will fill our data structure once it's well parsed
    lines = file_.readlines()
    for line in lines:
        parse_line(env, line)


def parse_stdin(env):
    """
        This func will parse Fact, rules and Queries in case the user choose to enter inputs by himself
        params :
            Env     : Env obj
        return :
            Nothing
    """

    print(SAKURA, "\nPlease enter your sets of Rules, Facts, Queries or all your modifications")
    print("Write \";;\" when you're done !\n", DEFAULT)

    while True:
        input_ = input()
        if input_ == ";;":
            return
        parse_line(env, input_)



def parse_input(params, env, first_iter):

    # matrix indexes pre-set so we just have to add columns
    if env.facts.facts_copy != None:
        env.facts.dict = env.facts.facts_copy
    if params.file and first_iter:
        parse_file(params, env)
    else:
        parse_stdin(env)

    env.init_rules() ### Init the rules obj with dict  key = rules string and value = None

    create_rules_trees(params, env)
    env.facts.facts_copy = copy.deepcopy(env.facts.dict) ### Save facts states before solving

    ### End of parsing
