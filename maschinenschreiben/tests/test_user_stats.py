import unittest
from maschinenschreiben.user_stats import UserStats

import datetime
import pandas as pd


class TestUserStats(unittest.TestCase):
    def test_load_user_stats(self):
        self.assertEqual(type(UserStats().load_user_stats()), pd.DataFrame)
        self.assertTrue(
            (['name', 'datetime', 'level', 'time', 'correctness', 'score'] == UserStats().stats.columns).all()
        )

    def test_get_last_state(self):
        stats = pd.DataFrame.from_dict(
            {
                'name': ['Anna', 'Berta', 'Anna'],
                'datetime': [1, 2, 3],#[datetime.datetime.now(), datetime.datetime.now(), datetime.datetime.now()],
                'level': [1, 2, 3],
                'time': [60, 70, 80],
                'correctness': [0.5, 0.7, 0.6],
                'score': [0.5, 0.7, 0.55],
            }
        )
        last_stats_anna = UserStats.get_last_state(stats=stats, username='Anna')
        self.assertEqual(last_stats_anna['name'], 'Anna')
        self.assertAlmostEqual(last_stats_anna['level'], 3)
        self.assertAlmostEqual(last_stats_anna['score'], 0.55)

        last_stats_berta = UserStats.get_last_state(stats=stats, username='Berta')
        self.assertAlmostEqual(last_stats_berta['correctness'], 0.7)
