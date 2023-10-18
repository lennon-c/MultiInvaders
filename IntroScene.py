# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:39:37 2023

@author: carol
"""

from SharedAssetsScenes import Scene

from Assets import Display, Square, Pane, Asset, Text
from Helpers import selected, single_choice
from Constants import c
import pygame


class Intro(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.id = 'intro'
        self.status = None
        pygame.display.set_caption('Multi Space Invaders')

        def warning(bub_text):
            """Warning text in intro."""

            display = pygame.display.get_surface()
            w, h = display.get_size()

            size = Text( self.window , 'Choose at least\none number!'
                             , h_align =0 , v_align=1
                             , height = 30, margin =  1
                             , wrap = True, adjust_size = True
                             , fontsize = self.fontsize_small
                               , fontcolor = 'blue'
                                , color = bub_text.color # color is importan
                             , **self.text_options)
            
            print('width', size.rect.width)
            print('height', size.rect.height)


            title = Text( bub_text , ''
                             , h_align =1 , v_align=1
                              , width =size.rect.width
                             , height = size.rect.height, margin =  1
                             , wrap = True, adjust_size = False
                             , fontsize = self.fontsize_small
                             , fontcolor = 'blue'
                             , color = bub_text.color # color is important,  previouse texts are visible
                             , **self.text_options)
            bub_text.include_aligned(title, margin =10, adjust_size = True)

            return title

        size = tuple( x*0.95 for x in self.window.get_size() )
        
        # bubble will not be printed
        bubble  = Square(self.window, '', size , 'blue', border_radius = self.border_radius)
        bubble.align('center')

        self.assets = self.shared_assets(bubble)
        self.assets = list(self.assets)  + self.intro_assets(bubble)

        # game and speed
        pane_gs = Pane(bubble, (10,10) )
        Asset.grid(2,1, pane_gs,  [self.bub_games, self.bub_speed ], margin=10, outer_margin= 0)
        
        # numbers and warning
        pane_nw = Pane(bubble, (10,10) )
        # warning
        self.bub_warning  = Square(pane_nw, '', (10,10), c('palette')[2] , border_radius = self.border_radius) # paleturquoise1 'olivedrab2'
        self.warning  = warning(self.bub_warning )
        
        Asset.grid(2,1, pane_nw,  [self.bub_numbers, self.bub_warning ], margin=10, outer_margin= 0)
        self.bub_warning.align('centerx')
     
        # (numbers, warning), (game and speed), avatars  
        pane_nga = Pane(bubble, (10,10) )
        Asset.grid(1,3, pane_nga,  [pane_nw, pane_gs, self.bub_avatars ], margin=10, outer_margin= 0)

        # buttons, (numbers, warning), (game and speed), avatars  
        panefinal = Pane(bubble, (10,10) )
        Asset.grid(2, 1, panefinal,  [self.bub_buttons, pane_nga], margin=10, outer_margin= 5)
        
        self.bub_buttons.align('centerx')

        # title, buttons, (numbers, warning), (game and speed), avatars  
        container = Pane(self.window, (10,10))
        Asset.grid(2, 1, container,  [self.bub_title, panefinal ], margin=10, outer_margin= 0)
        
        bubble.include_aligned(container, adjust_size=True, margin= 10)
        container.align('center')
        self.bub_title.align('centerx')
        bubble.align('center')

        self.assets = self.assets + [self.bub_warning, self.warning ]

        self.screen_mgr = Display(self.window, *self.assets )
        self.screen_mgr.update()

        self.home_button.disable()
        self.home_button.state  = 'disabled'


    def enter(self, data):
        self.home_button.disable()
        self.home_button.state  = 'disabled'
        self.sound_button.on = self.data_dic['sound']


    def leave(self):
        pass 
        # self.data_dic['selected_numbers'] = self.selected_numbers
        # self.data_dic['selected_speed'] = self.selected_speed
        # avatar = self.avatars[self.selected_avatar]
        # self.data_dic['selected_avatar'] = avatar.file
        # self.data_dic['selected_game'] = self.selected_game
        # self.data_dic['sound'] = self.sound_button.on

    def handle(self, events, keys_down):
        for event in events:
            self.shared_handle( event)

            if self.start_button.handle(event):
                self.go_to('play' )

            for square in self.squares.values():
                selected(event, square)

            for game in self.games.values():
                single_choice(event, game, self.games.values())

            for speed in self.speeds.values():
                single_choice(event, speed, self.speeds.values())

            for avatar in self.avatars.values():
                single_choice(event, avatar, self.avatars.values())


    def update(self):
        self.selected_numbers = [n for n, square in self.squares.items() if square.selected ]
        if len(self.selected_numbers) > 0:
            # selected = [str(n) for n  in self.selected_numbers]
            # text = (f'Selected:  {", ".join(selected)}')
            self.warning.set_text('')
            self.bub_warning.visible = False
            self.warning.visible = False

            for obj in self.start_button, self.history_button:
                obj.enable()
                # state is given by mouse movements when enable


        else:
            # self.score_text.set_text( f'Score: {self.game.score}' )
            self.warning.set_text('Choose at least one number!' )
            self.bub_warning.visible = True
            self.warning.visible = True

            for obj in self.start_button, self.history_button:
                obj.disable()
                obj.state = 'disabled'


        self.selected_speed = [level for level, obj in self.speeds.items() if obj.selected][0]
        self.selected_avatar = [level  for level, obj in self.avatars.items() if obj.selected][0]
        self.selected_game = [level for level, obj in self.games.items() if obj.selected][0]
        
        self.data_dic['selected_numbers'] = self.selected_numbers
        self.data_dic['selected_speed'] = self.selected_speed
        avatar = self.avatars[self.selected_avatar]
        self.data_dic['selected_avatar'] = avatar.file
        self.data_dic['selected_game'] = self.selected_game


    def draw(self):
        self.window.fill(c('palette')[1])
        self.screen_mgr.draw()

        for obj in  list(self.squares.values()) + list(self.speeds.values()) + list(self.avatars.values()) +  list(self.games.values()) :
            if obj.selected == True:
                obj.color = c('palette')[4]
            else:
                obj.color = 'white'
            obj.draw(canvas = self.window)



#%% TESTING
 
"""
pygame.quit()

"""
