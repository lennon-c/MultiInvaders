# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:43:50 2023

@author: carol
"""


#%% Initiate git
# open Gitbash in game folder and write commands

"""
git init
"""

#%% confi

print('git config --global user.email "14179052+lennon-c@users.noreply.github.com"')
print('git config --global user.name "Carolina Lennon"')
        
#%% gitignore
"""
touch .gitignore 
"""
ignore=[ 
        'HighScores.json',
        'UserSetting.json',
        'GameSharing/',
        '__pycache__/'
        ]

# set game folder as working directory in python
with open('.gitignore ', 'w') as f :
    for i in ignore:
        f.write(i + "\n") 
 
    
