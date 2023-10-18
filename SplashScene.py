# -*- coding: utf-8 -*-
"""
Created on Wed Mar 22 18:19:07 2023

@author: carol
"""

from Helpers import window_init, exit_event
from Assets import Text, Square, Display, Asset, PaneImage, Button
from Constants import c
import pygame
import os


colors = dict(default= 'cyan'
                        , hover =   c('palette')[3]
                        , pressed = c('palette')[1]
                        , disabled = (220, 220, 220))


def splash():
    """Splash window; only shown in the first at installation."""
    #### ASSETS
    # display
    size = (c('width_window'), c('height_window'))
    screen = window_init( size , c('palette')[1])

    # text area
    color = 'white'
    bubble = Square(screen, '',  size , color, border_radius= c('border_radius'))
    bubble_small1 = Square(bubble, '',  (10,10) , c('palette')[2] , border_radius= c('border_radius'))
    bubble_small2 = Square(bubble, '',  (10,10) ,  c('palette')[3], border_radius= c('border_radius'))

    # text lines
    name = c('name')
    texts0 = ['A shortcut to the game was created in your folder!' ]
    texts1 = [ 'It should look like:'
            , f'"{name}"' ]
    texts2 = [ 'You have two options:'
        ,  '1. You can simply double-click the shortcut to start playing the game right away.'
        ,  '2. If you prefer to have the shortcut in a different location, you can copy the shortcut to a location of your choice.'
        ]

    # texts to object
    w,h = size
    texts_objs0 = [ Text(bubble,text, width = w*0.8
                         , h_align = 1 , adjust_size = True
                         , fontcolor = 'blue'
                         , fontsize = c('fontsize_medium')  # c('fontsize')
                         , fontname =  c('fontname')) for text in texts0]

    texts_objs1 = [ Text(bubble_small1,text, width = w*0.7
                         , h_align = 1, adjust_size = True
                         , fontsize = c('fontsize_medium')
                          , fontcolor = 'blue'
                         , fontname =  c('fontname')) for text in texts1]

    texts_objs2 = [ Text(bubble_small2,text, width = w*0.7
                         , h_align = 0, adjust_size = True
                         , fontcolor = 'blue'
                         , fontsize = c('fontsize_medium')
                         , fontname =  c('fontname')) for text in texts2]

    # create icon object
    text = texts_objs0[0]
    icon = os.path.join(c('images_path'), 'icon.svg')
    image = PaneImage(bubble, (text.line_h, text.line_h), icon)
    print(text.line_h)

    # grids
    Asset.grid(3, 1 ,  bubble_small1 ,texts_objs1  + [image] ,  margin = 2, outer_margin=10 )
    Asset.grid(3, 1 ,  bubble_small2 ,texts_objs2 ,  margin = 2, outer_margin=10 )

    # final grid
    # create exit button
    button = Button(screen, text = 'Close me !', adjust_size= True, colors = colors
                    , fontname =  c('fontname')
                    , fontsize = c('fontsize_medium'))

    objets = texts_objs0 + [bubble_small1, bubble_small2] + [button]
    Asset.grid(len(objets), 1 ,  bubble,  objets ,  margin = 10, outer_margin=10)

    # some alignments
    bubble.align('center')
    bubble_small1.align('centerx')
    bubble_small2.align('centerx')
    button.align('centerx')
    image.align('centerx')

    # what to show
    objects = ([bubble, bubble_small1, bubble_small2 ]
               + texts_objs0 + texts_objs1
               + texts_objs2 + [image] +[button]
               )
    disp = Display(screen, *objects)


    #### LOOP
    running = True
    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():
            if exit_event(event):
                running = False
            if button.handle(event):
                running = False

        disp.update()
        disp.draw()

        pygame.display.flip()
        
    pygame.quit()

#%% TESTING

if (__name__ == '__main__'):
    splash()





