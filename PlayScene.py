
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  6 13:39:37 2023

@author: carol
"""
from Assets import Display
from SharedAssetsScenes import Scene

import pygame

from Constants import c
from Game import Game_mgr
from Helpers import  dragging_event, single_choice
from datetime import datetime


class Play(Scene):

    def __init__(self, window):
        super().__init__(window)

        self.id = 'play'
        self.status = 'not_yet_started'
        # ['not_yet_started','answered', 'not_answered']

        self.assets =  self.play_assets()
        self.screen_mgr = Display(self.window, *self.assets  )
        self.screen_mgr.update()


    def enter(self, data) :
        # print(data)
        self.home_button.visible = True
        self.start_button.enable()
        self.score_text.set_text( ' ' )
        self.last_answer.set_text( ' ' )
        self.status = 'not_yet_started'
        
        self.sound_button.on = self.data_dic['sound']
        img = pygame.image.load(self.data_dic['selected_avatar'])
        img = pygame.transform.smoothscale(img , c('avatar_play_size'))
        self.avatar_img.surface = img
        
        self.game = Game_mgr(self.window
                              , self.board
                             , self.data_dic['selected_numbers']
                             , self.data_dic['selected_speed']
                             , game = self.data_dic['selected_game'])
        self.game.variant =  self.data_dic['selected_variant']
        

    def leave(self) :
        self.status = 'not_yet_started'
        # self.data_dic['sound'] = self.sound_button.on
        today = datetime.now()
        self.score_data.add(self.game.score , self.data_dic['selected_avatar'], today.isoformat())
        self.game.score = 0


    def handle(self, events, keys_down):
        """
        handel the event loop
        """
        for event in events :
            self.shared_handle(event)

            for variant in self.variants.values():
                single_choice(event, variant, self.variants.values())

            # home button clicked
            if self.home_button.handle(event):
                self.go_to('intro')

            # play buttom clicked
            if self.start_button.handle(event) :
                # disable button
                self.start_button.disable() # irresposive
                self.start_button.state = 'disabled' # change image
                # start a question
                self.game.start()
                # set player on the bottom center of the mat
                self.game.player.rect.centery =   self.board.rect.bottom - c('circle_size')[1] // 2
                self.game.player.rect.centerx =   self.board.rect.centerx
                # hide introduction text from the mat
                self.middle_text.visible = False
                self.status = 'not_answered'

            # moving player with mouse
            if self.status == 'not_answered' and self.game.over == False:
                dragging_event(event,self.game.player,self.board)

            # mouse visibility
            if event.type == pygame.MOUSEMOTION :
                if self.status == 'not_yet_started' : # if not yet playing
                    pygame.mouse.set_visible(True)
                elif event.pos[1] > self.bub_buttons.rect.top: # if mouse in bottom panel
                    pygame.mouse.set_visible(True)
                else:
                    pygame.mouse.set_visible(False)  # playing and not at the bottom


    def update(self):
        # check if collided, missed, starting a new question needed using game.update()
        if self.status != 'not_yet_started' :
            self.game.update()

        # update score text
        if self.status != 'not_yet_started' :
            # print(self.game.score)
            self.score_text.set_text( f'Score: {self.game.score}' )
            try:
                self.last_answer.set_text( f'Last answer:{chr(10)}{self.game.last_answer}' )
            except:
                self.last_answer.set_text( '' )
            # print(self.score_text.text)
            self.game.sound = self.sound_button.on

        else:
            self.middle_text.visible = True

        self.selected_variant = [level for level, obj in self.variants.items() if obj.selected][0]
        self.game.variant = self.selected_variant
        self.data_dic['selected_variant'] = self.selected_variant
        
    def draw(self):
        """
        draw scree object at the end of each frame
        """
        self.window.fill('white')

        if self.status != 'not_yet_started' :
            self.game.draw()

        self.screen_mgr.draw()





#%% TESTING

if (__name__ == '__main__'):
    from Helpers import window_init, loop

    window_size = (c('width_window'), c('height_window'))
    window = window_init(size=window_size, color='red')
    aPlay = Play(window)
    aPlay.screen_mgr.draw()
    loop()





