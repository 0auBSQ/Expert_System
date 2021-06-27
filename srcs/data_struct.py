from srcs.const import *
from enum import Enum

class Setup():
    """
        Class used to store all the setup with :
            modify : Bool (accept or not to start again the same process with new facts and queries)
            visual : Bool (activate the visual mod to describe each step of the solver)
            file : String (path of the input file (if no path given, we read on the STDIN))
    """

    def __init__(self, modify, visual, display, file_):
        self.modify = modify
        self.visual = visual
        self.display = display
        self.file = file_
        pass

class Env():
    """
        This class regroup all the other data structures used to process the Query
            facts : class Facts()
            adj_matrix : pandas.DataFrame with rules as columns and facts as indexes, values are 0 or 1
            queries : list of all queries
            rules : TODO

    """

    def __init__(self, facts, rules, adj_matrix):
        self.facts = facts
        self.rules = rules
        self.adj_matrix = adj_matrix
        self.queries = []
        self.verbose = True

    def init_rules(self):
        for elem in self.adj_matrix.columns.values:
            self.rules.dict[elem] = None




class Facts():
    """
        All facts are stored in this class as a dict
            dict : dictionnary with the name of the fact as Key and the stat as value which is an enum
            enum : Enum used to store the state an the id of the state of a fact
    """

    def __init__(self):
        self.enum = Enum('state', 'FALSE_UNSET, FALSE, TRUE, UNDEFINED')
        self.dict = self.init_facts()
        self.facts_copy = None

    def init_facts(self):
        facts = {}
        for elem in ALL_FACTS:
            facts[elem] = self.enum['FALSE_UNSET']
        return facts

class Rules():

    def __init__(self):
        self.dict = {}
