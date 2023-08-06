from . import node


operators = {
    "and": node.AndNode,
    "or": node.OrNode,
    "not": node.NotNode
}
