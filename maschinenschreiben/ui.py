import time
import datetime
import numpy as np

from maschinenschreiben.lecture_generation import Lecture
from maschinenschreiben.dictionary import Dictionary
from maschinenschreiben.user_stats import UserStats


class UserInterface(object):
    def __init__(self, username='', level=0):
        self.dic = Dictionary()
        self.user_stats = UserStats()
        self.username = username
        self.level = level

    def welcome_message(self):
        print()
        print("Willkommen zum Maschinenschreiben-Lernprogramm.")

        # If user-stats exist, load them and present a choice:
        if len(self.user_stats.stats) > 0:
            print("Bitte such deinen Benutzernamen aus, oder gib einen neuen ein:")

            name_lookup = {str(k): name for k, name in enumerate(self.user_stats.get_usernames())}

            for k, name in name_lookup.items():
                print('{} - {}'.format(k, name))
            print()
        
            choice = input('Auswahl: ')

            if choice in name_lookup.keys():
                self.username = name_lookup[choice]
            else:
                self.username = choice

        # Otherwise just ask for a username:
        else:
            self.username = input('Bitte Benutzernamen eingeben: ')

    def choose_level(self):
        print()
        if self.username in self.user_stats.stats.name.unique():
            last_state = self.user_stats.get_last_state(stats=self.user_stats.stats, username=self.username)
            print("Dein letztes Übungslevel war {} (0-{}), mit einem Score von {:.1f} (0 - 100).".format(
                last_state['level'], self.dic.max_level, last_state['score']
            ))
        
        else:
            print("Für einen neuen Nutzer empfehlen wir Level 0.")
        
        self.level = np.clip(int(input('Gewünschtes Level (0-{}): ').format(self.dic.max_level)), 0, self.dic.max_level, dtype=int)
        self.lecture = Lecture(dic=self.dic, level=self.level)

    def lecture_loop(self):
        wants_lecture = True
        while wants_lecture:
            print()
            print('Bitte tippe folgende Worte möglichst genau und möglichst schnell ab:')
            print()
            lecture = ' '.join(self.lecture.create_lecture())
            print(lecture)
            start_time = time.time()
            print()
            students_answer = input()
            time_elapsed = time.time() - start_time

            # Now rate and score the students answer and give him/her feedback:
            correctness, time_elapsed, score = self.lecture.score_lecture(lecture, students_answer, time_elapsed)
            print()
            print('Du hast die Lektion in {:.0f} Sekunden abgeschlossen und dabei eine Korrektheit von {:.1f} (0-100) erreicht.'.format(time_elapsed, correctness))
            print('Deine Gesamtpunktzahl beträgt damit {:.0f} (0 - 100).'.format(score))

            # If the score is high enough and we are not yet at max_level, recommend a higher level:
            if score >= 80 and self.level < self.dic.max_level:
                print()
                self.level += int('j' in input('Deine Punktzahl ist hoch genug, um ein Level von {} auf {} aufzusteigen. Möchtest du das? (j/n) '.format(self.level, self.level + 1)))
                self.lecture = Lecture(dic=self.dic, level=self.level)

            # Store the lecture and the scores and save the user-stats:
            self.user_stats.add_and_save_stats(
                name=self.username,
                datetime=datetime.datetime.now(),
                level=self.level,
                time=time_elapsed,
                correctness=correctness,
                score=score,
            )

            print()
            wants_lecture = 'n' not in input("Noch eine Lektion? (j/n): ")
    