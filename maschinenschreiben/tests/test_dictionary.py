import unittest
from maschinenschreiben.dictionary import Dictionary


class TestDictionary(unittest.TestCase):
    def setUp(self):
        self.dic = [
            'abcd',
            'affe',
            'a0'
        ]
        self.curriculum = 'abcd01234'
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
        return True

    def test_create_level_corpus(self):
        # Todo
        return True


if __name__ == '__main__':
    unittest.main()