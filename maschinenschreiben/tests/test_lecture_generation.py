import unittest
from maschinenschreiben.lecture_generation import Lecture
from maschinenschreiben.dictionary import Dictionary


class TestLectureGeneration(unittest.TestCase):
    def setUp(self):
        corpus = [
            'Affe',
            'Banane',
            'Cholera',
            'Diphthong'
        ]
        bag_of_letters = ''.join(sorted(set(''.join([w for w in corpus]))))

        # Create a dictionary and override the values in it:
        dic = Dictionary(
            filename=None,
            seed={
                'curriculum': [bag_of_letters],
                'dic': corpus,
            },
            verbose=False
        )

        self.lecture = Lecture(
            dic=dic,
            level=0,
            length=20,
        )

    def test_lecture_generation(self):
        lecture = self.lecture.create_lecture(self.lecture.corpus, self.lecture.length)
        self.assertEqual(type(lecture), list)
        self.assertEqual(len(lecture), self.lecture.length)

    def test_analyse_lecture_histogram(self):
        lecture = ['aaa', 'ac', 'c']
        bag_of_letters = 'abc'
        histogram = Lecture.analyse_lecture_histogram(lecture=lecture, bag_of_letters=bag_of_letters)
        self.assertAlmostEqual(histogram['a'], 2/3)
        self.assertAlmostEqual(histogram['b'], 0.0)
        self.assertAlmostEqual(histogram['c'], 1/3)

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
