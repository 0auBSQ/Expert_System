from srcs.const import DEFAULT
from ete3 import Tree
from srcs.const import *

def visu_tree(tree, line):
    test = str(tree).replace("Tree", "").replace("[", "").replace("]", "").replace("'", "").replace("Token", "")
    test = test.replace("LETTER, ", "").replace("ARROW, ", "").replace("start, ", "") + ";"
    print(YELLOW, "Rule displayed : ", DEFAULT, line)
    Tree(test).show()

def print_tree(tree):
    print(tree.pretty())
    
