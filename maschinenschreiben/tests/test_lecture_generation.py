import unittest
from maschinenschreiben.lecture_generation import Lecture


class TestLectureGeneration(unittest.TestCase):
    def setUp(self):
        corpus = [
            'Affe',
            'Banane',
            'Cholera',
            'Diphthong'
        ]
        self.lecture = Lecture(corpus=corpus, length=20)

    def test_lecture_generation(self):
        lecture = self.lecture.create_lecture(self.lecture.corpus, self.lecture.length)
        self.assertEqual(type(lecture), list)
        self.assertEqual(len(lecture), self.lecture.length)

    def test_check_inclusion(self):
        # Word and curriculum are identical:
        #self.assertTrue(Lecture.check_inclusion('asdf', ''.join(sorted('asdf'))))

        # Word is included in the more comprehensive curriculum:
        #self.assertTrue(Lecture.check_inclusion('asdf', ''.join(sorted('asdfgqwer'))))

        # The word contains a character, that is not in the curriculum:
        #self.assertFalse(Lecture.check_inclusion('asdf', ''.join(sorted('asd_qweurip'))))
        return None


if __name__ == '__main__':
    unittest.main()
