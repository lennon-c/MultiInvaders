# -*- coding: utf-8 -*-
"""
Created on Mon Sep 18 10:35:20 2023

@author: carol
"""

import os
from Constants import c
import json

class UserSetting():
    """Manage user settings of the game.

    User setting are set by default in the first run after installation. But settings are changed based on user's selections and the game remembers the last selected options of the user, which are saved in the 'UserSetting.json' file.
    """

    def __init__(self):
        """Set default settings if no file is found (first game after installation) or retreive settings from file if it exists."""
        self.file = os.path.join(c('root'), 'UserSetting.json')
        if not os.path.exists(self.file):
            self.reset()  # set self.settings as an empty dict and creates a json file
            return
        # otherwise use json from disc
        with open(self.file, 'r') as f:
            self.settings = json.load(f)

    def save(self):
        """Save settings in file"""
        with open(self.file, 'w') as f:
            json.dump(self.settings, f)

    def reset(self):
        """Return to default settings and save in file."""
        self.settings = c('settings')
        self.save()


# %% TEST

if (__name__ == '__main__'):
    print('debbuging')
    settings = UserSetting()
    settings.reset()
    settings.settings
