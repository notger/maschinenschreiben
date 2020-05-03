# Defines methods to generate a specific lecture, given the level of the learner
# and a corpus of words. The level of the learner is defined by the letters allowed
# for word generation ("bag of letters").


class Lecture(object):
    def __init__(self, level):
        self.level = level

    def create_lecture(self, corpus, number_of_letters):
        # Creates a lecture with a given number of letters.

        # Pick a few words that are eligible.

        # Fill them up with random stuff, just to make sure we have covered everything.

        return None

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
