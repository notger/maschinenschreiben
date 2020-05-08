# Defines methods to generate a specific lecture, given the level of the learner
# and a corpus of words. The level of the learner is defined by the letters allowed
# for word generation ("bag of letters").
import numpy as np
from collections import Counter


class Lecture(object):
    def __init__(self, dic, level, length=20, verbose=False):
        self.dic = dic
        self.level= level
        self.length = length

        # For internal use and easier legibility:
        self.bag_of_letters = self.dic.eligible_letters_per_level[level]

        # Create the corpus for this level:
        self.corpus = dic.create_level_corpus(
            level=level, verbose=verbose
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
        lecture += self.generate_random_corpus(
            number_of_words=N_random, 
            histogram=self.analyse_lecture_histogram(
                lecture, bag_of_letters=self.bag_of_letters
            ), 
            word_length=5
        )

        # Now jumble them around randomly:

        return lecture

    @staticmethod
    def analyse_lecture_histogram(lecture=None, bag_of_letters=None):
        # Analyses the distribution of keystrokes in a given lecture to see whether we have some
        # underused ones.
        # Returns a dictionary containing all letters in bag_of_letters and their probability.

        # First, collect all letters and put them in a dictionary:
        all_letters = [a for a in ''.join(lecture)]

        # Count them:
        ctr = Counter(all_letters)

        # Manipulate the values to be probabilities:
        for key, value in ctr.items():
            ctr[key] = value / len(all_letters)

        # Add letters that did not show up in the lecture:
        for letter in bag_of_letters:
            if letter not in ctr.keys():
                ctr[letter] = 0.0

        return ctr

    @staticmethod
    def generate_random_corpus(number_of_words=None, histogram=None, word_length=None):
        # Generates random words from underused keys.
        random_corpus = [] 
        for k in range(number_of_words):
            random_corpus.append('asfd')
        return random_corpus

    # def check_inclusion(self, word, curriculum):
    #     # Checks whether the letters of a given dictionary-word are found in a bag of letters.
    #     return ''.join(sorted(word)) in curriculum
