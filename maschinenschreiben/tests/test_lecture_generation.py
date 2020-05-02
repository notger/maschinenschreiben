import unittest
from maschinenschreiben.lecture_generation import check_inclusion


class TestLectureGeneration(unittest.TestCase):
    def test_check_inclusion(self):
        # Word and curriculum are identical:
        self.assertTrue(check_inclusion('asdf', ''.join(sorted('asdf'))))

        # Word is included in the more comprehensive curriculum:
        self.assertTrue(check_inclusion('asdf', ''.join(sorted('asdfgqwer'))))

        # The word contains a character, that is not in the curriculum:
        self.assertFalse(check_inclusion('asdf', ''.join(sorted('asd_qweurip'))))


if __name__ == '__main__':
    unittest.TestCase.main()
