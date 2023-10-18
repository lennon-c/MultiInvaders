# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 15:25:17 2023

@author: carol
"""
from SplashScene import splash
from Installer import first_run_setup
from Constants import c, root
from Scenes import Scene_mgr
from IntroScene import Intro
from PlayScene import Play
from HighScoresScenes import HighScores
import sys

from babel.dates import format_timedelta
import babel.numbers


#### FROM THE EXECUTABLE
print(f'Home directory: {root()}')
# Check if the script is running from a frozen executable 
if not c('onefile'):
    if getattr(sys, 'frozen', False):
        first_time = first_run_setup(root(), splash)
        if first_time:
            sys.exit()
        

#### GAME
fps = 60
scenes  = [Intro, Play, HighScores]
size = (c('width_window'), c('height_window'))
 
scenes_mgr = Scene_mgr(scenes, size, fps)
scenes_mgr.run()

"""
pygame.quit()
quit()
"""

 