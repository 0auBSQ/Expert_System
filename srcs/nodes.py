import lark

def create_rules_trees(env):
    ### Pour acceder a la mémoire de l'arbre
    ### https://lark-parser.readthedocs.io/en/latest/classes.html#tree

    grammar = """
        start: operation ARROW operation
        leaf: LETTER
        parenthesis.6: "(" operation ")"
        unary.5: "!" operation
        and.4: operation AND operation
        or.3: operation OR operation
        xor.2: operation XOR operation
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
    p = lark.Lark(grammar)
    for element in env.adj_matrix.columns.values:
        env.rules.dict[element] = p.parse(element)
    