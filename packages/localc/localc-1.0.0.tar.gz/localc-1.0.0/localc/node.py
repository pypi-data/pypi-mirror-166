space = '     '
branch = '│    '
tee = '├─── '
last = '└─── '


def to_string(op_name: str, prefix: list, *operands):
    prefix_str = "".join(prefix)

    if prefix:
        prefix[-1] = branch if prefix[-1] == tee else space

    result = prefix_str + op_name + "\n"

    for operand in operands:
        if operand is not operands[-1]:
            result += operand.to_string(prefix + [tee]) + '\n'
        else:
            result += operand.to_string(prefix + [last])

    return result


class Node:
    def __init__(self, value=None):
        if isinstance(value, str):
            value = True if value == "true" else False
        elif value is None or isinstance(value, bool):
            pass
        else:
            raise Exception("Unsupported value")
        self.value = value

    def calc(self):
        if self.value is not None:
            return self.value
        else:
            raise Exception("Can't calc an empty Node")

    def __bool__(self):
        return self.calc()

    def __repr__(self):
        return "Node({0})".format(repr(self.value))

    def to_string(self, prefix):
        prefix_str = "".join(prefix)
        return str(self.value) if not prefix else prefix_str + str(self.value)

    def __str__(self):
        return self.to_string([])


class IdentifierNode(Node):
    identifiers = {}

    def __new__(cls, name=None, *args, **kwargs):
        if name in IdentifierNode.identifiers:
            return IdentifierNode.identifiers[name]
        else:
            instance = super().__new__(cls)
            IdentifierNode.identifiers[name] = instance
            return instance

    def __init__(self, name=None, value=None):
        self.name = name
        if value is not None:
            Node.__init__(self, value)
        elif "value" in dir(self) and isinstance(self.value, bool):  # test if there's a bool value already
            pass
        else:
            Node.__init__(self)

    def calc(self):
        if self.value is not None:
            return self.value
        else:
            raise Exception("Can't calc a value with an unspecified identifier")

    def to_string(self, prefix):
        prefix_str = "".join(prefix)
        if self.value is None:
            name = "[ {} ]".format(self.name)
        else:
            name = "[ {} -> {} ]".format(self.name, self.value)
        return name if not prefix else prefix_str + name

    def __repr__(self):
        if self.value is None:
            return "IdentifierNode(\"{}\")".format(self.name)
        else:
            return "IdentifierNode(\"{}\", {})".format(self.name, self.value)

    def set_value(self, value: bool):
        assert isinstance(value, bool) or value is None, \
            "an identifier can only have a bool value"
        self.__dict__['value'] = value

    def get_value(self):
        return self.__dict__['value']

    value = property(get_value, set_value)


class GroupNode(Node):
    def __init__(self, sub_node: Node):
        self.sub_node = sub_node
        Node.__init__(self)

    def calc(self):
        return self.sub_node.calc()

    def __bool__(self):
        return self.sub_node.calc()

    def __repr__(self):
        return "GroupNode({0})".format(repr(self.sub_node))

    def to_string(self, prefix):
        return to_string("GROUP", prefix, self.sub_node)


class AndNode(Node):
    def __init__(self, operand1, operand2):
        if not isinstance(operand1, Node):
            operand1 = Node(operand1)
        if not isinstance(operand2, Node):
            operand2 = Node(operand2)
        self.operand1 = operand1
        self.operand2 = operand2
        Node.__init__(self)

    def calc(self):
        self.value = self.operand1.calc() and self.operand2.calc()
        return self.value

    def __repr__(self):
        return "AndNode({0}, {1})".format(repr(self.operand1), repr(self.operand2))

    def to_string(self, prefix):
        return to_string("AND", prefix, self.operand1, self.operand2)


class OrNode(Node):
    def __init__(self, operand1, operand2):
        if not isinstance(operand1, Node):
            operand1 = Node(operand1)
        if not isinstance(operand2, Node):
            operand2 = Node(operand2)
        self.operand1 = operand1
        self.operand2 = operand2
        Node.__init__(self)

    def calc(self):
        self.value = self.operand1.calc() or self.operand2.calc()
        return self.value

    def __repr__(self):
        return "OrNode({0}, {1})".format(repr(self.operand1), repr(self.operand2))

    def to_string(self, prefix):
        return to_string("OR", prefix, self.operand1, self.operand2)


class NotNode(Node):
    def __init__(self, operand):
        if not isinstance(operand, Node):
            operand = Node(operand)
        self.operand = operand
        Node.__init__(self)

    def calc(self):
        self.value = not self.operand.calc()
        return self.value

    def __repr__(self):
        return "NotNode({0})".format(repr(self.operand))

    def to_string(self, prefix):
        return to_string("NOT", prefix, self.operand)
