# -*- coding: utf-8 -*-
"""
Created on Sat Apr 22 20:23:38 2023

@author: carol
"""
import os
from Constants import c
import json


class ScoresData():
    """Manage list of scores.

    Scores are a list that is saved in a json file. User can reset the score and empty the list.
    Scores can also be updated (add).
    """

    N_HIGH_SCORES = 10

    # score, player_id (file) , date

    def __init__(self):
        """Create a list of scores or retrieve it from a json file."""
        self.file = os.path.join(c('root'), 'HighScores.json')
        if not os.path.exists(self.file):
            self.reset()  # set self.scores_list as an empty list and creates a json file
            return
        # otherwise use json from disc
        with open(self.file, 'r') as f:
            self.scores_list = json.load(f)

    def add(self, score, player_id, date):
        """ Add the new high score to the list if there are still free slots or if this game's score is better or equal than the worse score in previous games"""

        if score <= 0:  # only for positive new scores, if negative do nothing
            return

        # still free places? (current list smaller than max places to retain)
        if len(self.scores_list) < self.N_HIGH_SCORES:  # add
            self.scores_list.insert(0, [score, player_id,  date])
        else:
            # if the min score of previous games is smaller or equal to this game's score => add
            previous_min = min(self.scores_list)[0]
            if score >= previous_min:
                self.scores_list.insert(0, [score, player_id,  date])
            else:  # if no free places and no better score than the min, do nothing
                return

        # sorted descending by score (first element) and date (second), in case of a score tie delete older
        self.scores_list = sorted(
            self.scores_list, key=lambda x: (x[0], x[2]), reverse=True)
        # if we add more than the max spots allowed, delete last item
        if len(self.scores_list) > self.N_HIGH_SCORES:
            self.scores_list.pop()
        self.save()
        return

    def save(self):
        """Write score in json"""
        with open(self.file, 'w') as f:
            json.dump(self.scores_list, f)

    def reset(self):
        """Set an empty score list and save it as json"""
        self.scores_list = list()
        self.save()


# %% TEST

if (__name__ == '__main__'):

    data = ScoresData()
    data.add(10, 'carolina', '12.01')
    data.add(1, 'carolina', '13.01')
    data.add(1, 'carolina', '12.01')
    data.add(1, 'carolina', '12.01')
    data.add(-1, 'carolina', '12.01')
    data.add(2, 'fs', '12.01')

    data.reset()
