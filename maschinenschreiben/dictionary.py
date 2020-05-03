import numpy as np
from maschinenschreiben.level_definition import curriculum


class Dictionary(object):
    # Class to store all allowed words and their numerical embeddings.
    def __init__(self, filename='german.dic'):
        self.dic = self.load_dictionary(filename)

        # Based on the curriculum above, we construct the dictionary which contains the letters eligible per level.
        # Important: This list has to be sorted!
        self.eligible_letters_per_level = [
            ''.join(
                sorted(set(''.join(
                    curriculum[0:k + 1])
                ))
            ) for k in range(len(curriculum))
        ]

        # Create a letter to numbers and numbers to letters lookup for later use, e.g. embedding-conversion:
        self.letter_embedding_lookup = self.create_letter_embedding_lookup(curriculum[-1])

        # Create the one-hot-encoded representation:
        #self.embeddings = self.create_embedding(self.dic, self.eligible_letters_per_level[-1])

    @staticmethod
    def load_dictionary(filename):
        # Load the dictionary. We can load the dictionary as a list of words, to be used
        # for later filtering and selection:
        with open(filename, 'r') as f:
            # Load each line, but only take the part before the slash, if one exists.
            # Also ignore lines with a leading pound-symbol, as that might be a comment. ;)
            dic = [line.split('/')[0] for line in f.readlines() if line[0] != '#']

        return dic

    @staticmethod
    def create_letter_embedding_lookup(set_of_letters):
        # Creates a lookup from original letters to embeddings and vice versa.
        lookup = dict(
            zip(set_of_letters, range(len(set_of_letters)))
        )
        lookup.update(zip(range(len(set_of_letters)), set_of_letters))
        return lookup

    @staticmethod
    def create_embeddings(dic, set_of_letters, number_letter_lookup):
        # Create a second version of the dictionary with "embeddings". Each letter has one column
        # in a one-hot-encoding-matrix of dim N x M, where N is the number of words in the original
        # dictionary and M is the number of max allowed letters in the highest level:
        embeddings = np.zeros((len(dic), len(set_of_letters)))

        # Todo
        return embeddings

    @staticmethod
    def create_level_corpus(embeddings, level):
        # Creates the corpus for each level, as defined by the eligible letters per level.
        return []
