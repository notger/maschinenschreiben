import time
import unittest
import numpy as np
from maschinenschreiben.dictionary import Dictionary


class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.dic = [
            'abcd',
            'affe',
            'b03'
        ]
        self.curriculum = ['abcd', 'abcd0123']
        self.lookup = Dictionary.create_letter_embedding_lookup(self.curriculum[-1])
        self.embeddings = Dictionary.create_embeddings(self.dic, self.curriculum[-1], self.lookup)

    def test_load_dictionary(self):
        dic = Dictionary.load_dictionary('german.dic')
        self.assertGreater(len(dic), 10)

    def test_create_letter_embedding_lookup(self):
        curriculum = self.curriculum[-1]
        lookup = self.lookup
        self.assertEqual(len(lookup.keys()), 2 * len(curriculum))
        self.assertIn('a', lookup.keys())
        self.assertIn(0, lookup.keys())
        self.assertIn('0', lookup.keys())
        self.assertNotEqual(lookup[0], lookup['0'])

    def test_create_embedding(self):
        curriculum = self.curriculum[-1]
        self.assertEqual(self.embeddings.shape, (len(self.dic), len(curriculum) + 1))
        self.assertTrue((self.embeddings[0, :] == np.asarray([1, 1, 1, 1, 0, 0, 0, 0, 0])).all())
        self.assertTrue((self.embeddings[1, :] == np.asarray([1, 0, 0, 0, 0, 0, 0, 0, 1])).all())
        self.assertTrue((self.embeddings[2, :] == np.asarray([0, 1, 0, 0, 1, 0, 0, 1, 0])).all())

    def test_create_level_corpus(self):
        # Test the corpus on the full last curriculum, which should return the first and the third word
        # of the initial dic:
        corpus = Dictionary.create_level_corpus(self.dic, self.embeddings, self.curriculum[-1], self.lookup)
        self.assertIn('abcd', corpus)
        self.assertIn('b03', corpus)
        self.assertEqual(len(corpus), 2)
        
        # Test again for a more restrictive corpus which should only leave the last word left:
        corpus = Dictionary.create_level_corpus(self.dic, self.embeddings, 'b03', self.lookup)
        self.assertIn('b03', corpus)
        self.assertEqual(len(corpus), 1)

    def test_performance(self):
        start_time = time.time()
        dic = Dictionary(verbose=False)
        print("Performance-test: Creating Dictionary took {:.1f} s for {} entries.".format(time.time() - start_time, dic.embeddings.shape[0]))

        start_time = time.time()
        corpus = dic.create_level_corpus(dic.dic, dic.embeddings, dic.eligible_letters_per_level[-1], dic.letter_embedding_lookup, verbose=True)
        print("Performance-test: Creating a full corpus took {:.1f} s for {} entries.".format(time.time() - start_time, len(corpus)))


if __name__ == '__main__':
    unittest.main()