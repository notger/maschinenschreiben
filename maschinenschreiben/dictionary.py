import numpy as np
from maschinenschreiben.level_definition import curriculum


class Dictionary(object):
    # Class to store all allowed words and their numerical embeddings.
    # If you specify a filename to load, then this will be used.
    # Otherwise, you have to specify the seed in the following form:
    # seed = {
    #     'curriculum' = curriculum
    #     'dic' = a list of words
    # }
    def __init__(self, filename='german.dic', seed=None, verbose=True):
        if filename is not None:
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
        else:
            self.dic = seed.get('dic', None)
            self.eligible_letters_per_level = seed.get('curriculum', None)

        self.max_level = len(self.eligible_letters_per_level) - 1

        # Create a letter to numbers and numbers to letters lookup for later use, e.g. embedding-conversion:
        self.letter_embedding_lookup = self.create_letter_embedding_lookup(self.eligible_letters_per_level[-1])

        # Create the one-hot-encoded representation, if it does not already exist:
        # Check for file existence, then load, otherwise generate and save.
        self.embeddings = self.create_embeddings(self.dic, self.eligible_letters_per_level[-1], self.letter_embedding_lookup)
        
        if verbose:
            print("Loaded dictionary with {} entries.".format(len(self.dic)))
            print("After pruning the dictionary, {} entries remain.".format(self.embeddings.shape[0]))

    @staticmethod
    def load_dictionary(filename):
        # Load the dictionary. We can load the dictionary as a list of words, to be used
        # for later filtering and selection:
        with open(filename, 'r') as f:
            # Load each line, but only take the part before the slash or return, if one exists.
            # Also ignore lines with a leading pound-symbol, as that might be a comment. ;)
            dic = [line.split('/')[0].split('\n')[0] for line in f.readlines() if line[0] != '#']

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
    def create_embeddings(dic, set_of_letters, letter_embedding_lookup):
        # Create a second version of the dictionary with "embeddings". Each letter has one column
        # in a one-hot-encoding-matrix of dim N x (M+1), where N is the number of words in the original
        # dictionary and M+1 is the number of max allowed letters in the highest level plus one more
        # for catching letters that are not in the set of letters, e.g. scandinavian or french ones:
        embeddings = np.zeros((len(dic), len(set_of_letters) + 1), dtype=int)
        catch_all_index = embeddings.shape[1] - 1

        for k, word in enumerate(dic):
            ordered_letters = sorted(list(set(word)))
            # Create the list of indices from the word. If the word contains letters not allowed,
            # book them into the catch-all-column, which is the last one:
            indices = [letter_embedding_lookup.get(a, catch_all_index) for a in ordered_letters]
            embeddings[k, indices] = 1

        return embeddings

    def create_level_corpus(self, level, verbose=False):
        # Creates the corpus for each level, as defined by the eligible letters per level.
        catch_all_index = self.embeddings.shape[1] - 1
        indices_of_allowed_letters = [self.letter_embedding_lookup.get(a, catch_all_index) for a in self.eligible_letters_per_level[level]]

        # Now generate a mask over the embeddings E, such that when we multiply the mask 
        # and the embeddings, all non-allowed letters stand out. The mask M will contain a 1 for
        # each letter that is not allowed and a zero for allowed letters.
        # Thus, (M x E)_ij = 1 if a letter in E shows up, that should not be allowed and 0 otherwise.
        # So sum_i (M x E)_ij
        mask = np.ones_like(self.embeddings, dtype=int)
        mask[:, indices_of_allowed_letters] = 0
        unallowed_letters_present = np.sum(mask * self.embeddings, axis = 1)
        words_to_keep = np.where(unallowed_letters_present == 0)[0]
        corpus = [self.dic[i] for i in words_to_keep]

        if verbose:
            print("Created a corpus with {} entries.".format(len(corpus)))
    
        return corpus
