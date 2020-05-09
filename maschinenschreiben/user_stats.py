import pandas as pd


class UserStats(object):
    def __init__(self, filename='user_stats.csv'):
        self.field_list = ['name', 'datetime', 'level', 'time', 'correctness', 'score']
        self.filename = filename
        self.stats = self.load_user_stats()

    def load_user_stats(self):
        # Load the user stats file. If it does not exist, then create a user stats model.
        # For fun and giggles, we are doing this according to "ask for forgiveness, not permission":
        try:
            return pd.read_csv(self.filename)
        except FileNotFoundError:
            return pd.DataFrame(columns=self.field_list)

    def save_user_stats(self):
        self.stats.to_csv(self.filename)

    @staticmethod
    def get_last_state(stats=None, username=None):
        tmp = stats.query('name == "{}"'.format(username))
        if len(tmp) > 0:
            # Fun fact: This is ugly. If you use to_dict, normally it would give you the row-index
            # in the output: key: {row_index, value}. So you have to use the switch 'r' to give
            # row-wise output, but that will convert the output of to_dict to a list, so we have
            # to take the first element of that list. Bah.
            return tmp.tail(1).to_dict('r')[0]
        else:
            return None
