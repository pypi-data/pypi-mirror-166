import unittest
from localc.scanner import *
from localc.parser import *


class TestParser(unittest.TestCase):
    def test_priority(self):
        tokens = scan("false or true and false")
        # print(expression(tokens))
        self.assertFalse(expression(tokens).calc())
        tokens = scan("(not false or true and false) and true")
        # print(expression(tokens))
        self.assertTrue(expression(tokens).calc())

    def test_identifier_parse(self):
        tokens = scan("not p and q")
        root = expression(tokens)
        # print(root)
        self.assertEqual(repr(root), 'AndNode(NotNode(IdentifierNode("p")), IdentifierNode("q"))')

        tokens = scan("not p:true or q:true")
        root = expression(tokens)
        # print(root)
        self.assertEqual(repr(root), 'OrNode(NotNode(IdentifierNode("p", True)), IdentifierNode("q", True))')


if __name__ == '__main__':
    unittest.main()
