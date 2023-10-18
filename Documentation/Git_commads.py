# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 12:43:50 2023

@author: carol
"""


#%% Initiate git
# open Gitbash in game folder and write the command

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
        , 'Git_commads.py'
        ]

# set game folder as working directory in python
with open('.gitignore ', 'w') as f :
    for i in ignore:
        f.write(i + "\n") 
 
    
#%% Start tracking 
"""
git add *
git add  .gitignore
"""
#%% First commit 
def commit(comment, file = None):
    """Commit commad with commit message"""
    file_to_commit = file if file != None else  ''
    print(f'git commit {file_to_commit} -m "{comment}"' )


commit('Start')   
"""
git commit  -m "Start"
"""

#%% further commits

def commit_a(comment, file = None):
    """Commit commad with commit message and skip stage area"""
    file_to_commit = file if file != None else  ''
    print(f'git commit {file_to_commit} -a -m "{comment}"' ) 
    
    
commit_a('Add Git_commads to .gitignore')
# git commit  -a -m "Add Git_commads to .gitignore"
