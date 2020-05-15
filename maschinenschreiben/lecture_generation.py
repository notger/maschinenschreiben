# Defines methods to generate a specific lecture, given the level of the learner
# and a corpus of words. The level of the learner is defined by the letters allowed
# for word generation ("bag of letters").
import random
import numpy as np
import Levenshtein as lev
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

    def create_lecture(self, random_proportion=0.1):
        # Creates a lecture with a given number of words.
        N_regular = int((1 - random_proportion) * self.length)
        indices = list(range(len(self.corpus)))
        chosen_indices = np.random.choice(indices, N_regular).tolist()
        np.random.shuffle(chosen_indices)

        # Pick a few words that are eligible.
        lecture = [self.corpus[k] for k in chosen_indices]

        # Fill them up with random stuff, just to make sure we have covered everything.
        N_random = self.length - N_regular
        lecture += self.generate_random_lecture(
            number_of_words=N_random, 
            histogram=self.analyse_lecture_histogram(
                lecture, bag_of_letters=self.bag_of_letters
            ), 
            word_length=5
        )

        # Now jumble them around randomly and return them:
        random.shuffle(lecture)
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
    def generate_random_lecture(number_of_words=None, histogram=None, word_length=None):
        # Generates random words from underused keys.
        
        # Extract the weights from the histogram.
        # (In case you are wondering: We are not using bag_of_letters here as the histogram might have
        # its own ordering and we obviously need the correct ordering between letters and their probability.)
        letters = list(histogram.keys())
        weights = np.asarray(list(histogram.values()))

        # The weights at that point indicate the frequency of the letter in the lecture.
        # As we want to favour the less-presented letters, we will make the probability
        # of showing up proportional to 1 - weight:
        letter_likelihood = 1 - weights
        letter_likelihood /= np.sum(letter_likelihood)

        # Now we can create the random words:
        random_corpus = [] 
        for k in range(number_of_words):
            random_corpus.append(
                ''.join(
                    np.random.choice(letters, size=word_length, p=letter_likelihood)
                )
            )

        return random_corpus

    @staticmethod
    def score_lecture(lecture, answer, time_elapsed, expected_typing_speed=1.5):
        '''Score the lecture. Expected typing speed is keys per second.'''
        correctness = 100 * (1.0 - lev.distance(lecture, answer) / len(lecture))
        expected_time = len(lecture) / expected_typing_speed
        time_score = 100 * min(1.0, expected_time / time_elapsed)
        score = 0.5 * (time_score + correctness)
        return correctness, time_elapsed, score
