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
        self.curriculum = 'abcd0123'
        self.lookup = Dictionary.create_letter_embedding_lookup(self.curriculum)
        self.embeddings = Dictionary.create_embeddings(self.dic, self.curriculum, self.lookup)

    def test_load_dictionary(self):
        dic = Dictionary.load_dictionary('german.dic')
        self.assertGreater(len(dic), 10)

    def test_create_letter_embedding_lookup(self):
        curriculum = self.curriculum
        lookup = self.lookup
        self.assertEqual(len(lookup.keys()), 2 * len(curriculum))
        self.assertIn('a', lookup.keys())
        self.assertIn(0, lookup.keys())
        self.assertIn('0', lookup.keys())
        self.assertNotEqual(lookup[0], lookup['0'])

    def test_create_embedding(self):
        self.assertEqual(self.embeddings.shape, (len(self.dic), len(self.curriculum)))
        self.assertTrue((self.embeddings[0, :] == np.asarray([1, 1, 1, 1, 0, 0, 0, 0])).all())
        self.assertTrue((self.embeddings[1, :] == np.asarray([1, 0, 0, 0, 0, 0, 0, 0])).all())
        self.assertTrue((self.embeddings[2, :] == np.asarray([0, 1, 0, 0, 1, 0, 0, 1])).all())
        return True

    def test_create_level_corpus(self):
        # Todo
        return True


if __name__ == '__main__':
    unittest.main()