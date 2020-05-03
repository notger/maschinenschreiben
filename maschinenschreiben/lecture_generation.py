# Defines methods to generate a specific lecture, given the level of the learner
# and a corpus of words. The level of the learner is defined by the letters allowed
# for word generation ("bag of letters").
import numpy as np


class Lecture(object):
    def __init__(self, corpus, length=20):
        self.corpus = corpus
        self.length = length

    @staticmethod
    def create_lecture(corpus, length, random_proportion=0.1):
        # Creates a lecture with a given number of letters.
        N_regular = int((1 - random_proportion) * length)
        indices = list(range(len(corpus)))
        chosen_indices = np.random.choice(indices, N_regular).tolist()
        np.random.shuffle(chosen_indices)

        # Pick a few words that are eligible.
        lecture = [corpus[k] for k in chosen_indices]

        # Fill them up with random stuff, just to make sure we have covered everything.
        N_random = length - N_regular

        return lecture

    def analyse_lecture_histogram(self, corpus):
        # Analyses the distribution of keystrokes in a given lecture to see whether we have some
        # underused ones.
        return None

    def generate_random_corpus(self, lecture, weights, number_of_letters):
        # Generates random words from underused keys. 
        return None

    def check_inclusion(self, word, curriculum):
        # Checks whether the letters of a given dictionary-word are found in a bag of letters.
        return ''.join(sorted(word)) in curriculum
