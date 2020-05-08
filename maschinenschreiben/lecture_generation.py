# Defines methods to generate a specific lecture, given the level of the learner
# and a corpus of words. The level of the learner is defined by the letters allowed
# for word generation ("bag of letters").
import numpy as np


class Lecture(object):
    def __init__(self, dic, level, length=20):
        self.length = length
        self.dic = dic
        self.bag_of_letters = self.dic.eligible_letters_per_level[level]
        self.corpus = dic.create_level_corpus(
            dic.dic, dic.embeddings, self.bag_of_letters, dic.letter_embedding_lookup, verbose=True
        )

    def create_lecture(self, corpus, length, random_proportion=0.1):
        # Creates a lecture with a given number of letters.
        N_regular = int((1 - random_proportion) * length)
        indices = list(range(len(corpus)))
        chosen_indices = np.random.choice(indices, N_regular).tolist()
        np.random.shuffle(chosen_indices)

        # Pick a few words that are eligible.
        lecture = [corpus[k] for k in chosen_indices]

        # Fill them up with random stuff, just to make sure we have covered everything.
        N_random = length - N_regular
        lecture += self.generate_random_corpus(N_random, [], 5)

        # Now jumble them around randomly:

        return lecture

    @staticmethod
    def analyse_lecture_histogram(corpus):
        # Analyses the distribution of keystrokes in a given lecture to see whether we have some
        # underused ones.
        return None

    @staticmethod
    def generate_random_corpus(number_of_words, weights, word_length):
        # Generates random words from underused keys.
        random_corpus = [] 
        for k in range(number_of_words):
            random_corpus.append('asfd')
        return random_corpus

    # def check_inclusion(self, word, curriculum):
    #     # Checks whether the letters of a given dictionary-word are found in a bag of letters.
    #     return ''.join(sorted(word)) in curriculum
