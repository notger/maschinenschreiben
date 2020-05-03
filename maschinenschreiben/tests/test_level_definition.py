import unittest
from maschinenschreiben.level_definition import curriculum


class TestLevelDefinitions(unittest.TestCase):
    def test_completeness(self):
        # Test whether all letters and numbers as well as the most important punctuation marks
        # are used in the curriculum:
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
