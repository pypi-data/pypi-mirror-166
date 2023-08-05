import ast
import pathlib
import unittest

from autocomp import parse_file


class UtilTestCase(unittest.TestCase):

    def test_parse_file(self):
        cur = pathlib.Path(__file__).parent.joinpath('./test_utils.py')
        tree = parse_file(cur)
        self.assertIsInstance(tree, ast.AST)