from ete3 import Tree

def visu_tree(tree):
    test = str(tree).replace("Tree", "").replace("[", "").replace("]", "").replace("'", "").replace("Token", "")
    test = test.replace("LETTER, ", "").replace("ARROW, ", "").replace("start, ", "") + ";"
    Tree(test).show()

def print_tree(tree):
    print(tree.pretty())
    
