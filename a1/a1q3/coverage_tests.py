import unittest

from .token_with_escape import token_with_escape
from .token_with_escape_mutant1 import token_with_escape_mutant1
from .token_with_escape_mutant2 import token_with_escape_mutant2

class CoverageTests(unittest.TestCase):
    def test_statement_coverage(self):
        """Add tests to achieve statement coverage (as many as needed)."""
        # YOUR CODE HERE 
        print(token_with_escape('one^|uno||three^^^^|four^^^|^cuatro|'))
        pass

    def test_kill_mutant_1(self):
        """Kill mutant 1"""
        # YOUR CODE HERE
        result=print(token_with_escape_mutant1('one^|uno||three^^^^|four^^^|^cuatro|'))
        self.assertNotEquals(result, ['one|uno', '', 'three^^', 'four^|cuatro', ''] )
        pass

    def test_kill_mutant_2(self):
        """Kill mutant 2"""
        # YOUR CODE HERE
        result = token_with_escape_mutant2('one^|uno||three^^^^|four^^^|^cuatro|')
        self.assertNotEquals(result, ['one|uno', '', 'three^^', 'four^|cuatro', ''] )
        pass
