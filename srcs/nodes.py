import lark
from srcs.display_tree import visu_tree, print_tree

def create_rules_trees(env):
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
        print_tree(env.rules.dict[element]) ## Print the rules's tree in terminal
        visu_tree(env.rules.dict[element]) ## Display the rule's tree
    