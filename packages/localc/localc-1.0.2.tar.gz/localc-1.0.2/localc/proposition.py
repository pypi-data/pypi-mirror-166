from .node import *
from .operators import *
from .scanner import *
from .parser import *
from prettytable import PrettyTable


def _bin_enumerate(items: int):
    result = [False] * items
    for bin_result in range(2 ** items):
        for i in range(items):
            result[i] = bool((bin_result >> i) & 1)
        yield reversed(result)


def _add_every_step(root: Node, title: list):
    for operand_name, operand in root.__dict__.items():
        if operand_name.startswith("operand"):
            _add_every_step(operand, title)
    s = root.to_descriptive_string()
    if s not in title:
        title.append(s)


def _search_unspecified(root: Node, identifiers: list, unspecified: list):
    for operand_name, operand in root.__dict__.items():
        if operand_name.startswith("operand"):  # get operands
            if isinstance(operand, IdentifierNode) and operand not in identifiers:  # get new identifiers
                identifiers.append(operand)
                if operand.value is None:  # get unspecified identifiers
                    unspecified.append(operand)
            _search_unspecified(operand, identifiers, unspecified)


class Proposition:
    def __init__(self, statement):
        self._statement = statement
        self._tokens = scan(statement)
        self.root: Node = expression(self._tokens)
        self.identifiers = None
        self.unspecified = None
        self.table = None
        self.title = None
        self.init()

    def __repr__(self):
        return "Proposition(\"{}\")".format(self._statement)

    def __str__(self):
        return str(self.root)

    def calc(self):
        return self.root.calc()

    def init(self):
        self.identifiers = []
        self.unspecified = []
        if isinstance(self.root, IdentifierNode):
            self.identifiers = [self.root]
            if self.root.value is None:
                self.unspecified = [self.root]
        else:
            _search_unspecified(self.root, self.identifiers, self.unspecified)
        IdentifierNode.reset()

        self.table = PrettyTable()
        self.title = []
        _add_every_step(self.root, self.title)
        self.table.field_names = sorted(self.title, key=str.__len__)
