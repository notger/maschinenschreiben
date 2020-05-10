import unittest
from collections import Counter
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
        lecture = self.lecture.create_lecture()
        self.assertEqual(type(lecture), list)
        self.assertEqual(len(lecture), self.lecture.length)

    def test_analyse_lecture_histogram(self):
        lecture = ['aaa', 'ac', 'c']
        bag_of_letters = 'abc'
        histogram = Lecture.analyse_lecture_histogram(lecture=lecture, bag_of_letters=bag_of_letters)
        self.assertAlmostEqual(histogram['a'], 2/3)
        self.assertAlmostEqual(histogram['b'], 0.0)
        self.assertAlmostEqual(histogram['c'], 1/3)

    def test_generate_random_lecture(self):
        # Check the basic functionality of the function for a case which only allows for one character:
        lecture = Lecture.generate_random_lecture(
            number_of_words=2,
            histogram={'a': 1.0, 'b': 0.0},
            word_length=4,
        )
        self.assertEqual(['bbbb', 'bbbb'], lecture)

        # Check for a more complex case, that the underrated letters indeed are more likely:
        lecture = Lecture.generate_random_lecture(
            number_of_words=1000,
            histogram={'a': 2/5, 'b': 2/5, 'c': 1/5},
            word_length=1,
        )
        ctr = Counter(lecture)
        # All letters should be in:
        for letter in ['a', 'b', 'c']:
            self.assertIn(letter, ctr.keys())
        # c should have the highest count:
        self.assertGreater(ctr['c'], ctr['a'])
        self.assertGreater(ctr['c'], ctr['b'])


if __name__ == '__main__':
    unittest.main()
