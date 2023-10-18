# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 19:48:58 2023

@author: carol
"""


from Assets import Display
from SharedAssetsScenes import Scene
from Constants import c


class HighScores(Scene):

    def __init__(self, window):
        super().__init__(window)
        self.id = 'scores'

        self.assets = self.scores_assets()
        self.screen_mgr = Display(self.window, *self.assets)
        self.screen_mgr.update()

    def handle(self, events, keys_down):
        for event in events:

            if self.start_button.handle(event):
                self.go_to('play')

            if self.home_button.handle(event):
                self.go_to('intro')

            if self.garbage_button.handle(event):
                self.score_data.reset()

                self.assets = self.scores_assets()
                self.screen_mgr = Display(self.window, *self.assets)

                self.sound_button.on = self.data_dic['sound']
                self.screen_mgr.update()
                self.history_button.disable()
                self.history_button.state = 'disabled'

            self.shared_handle(event)

    def enter(self, data):
        self.assets = self.scores_assets()
        self.screen_mgr = Display(self.window, *self.assets)
        self.screen_mgr.update()
        self.sound_button.on = self.data_dic['sound']
        self.history_button.disable()
        self.history_button.state = 'disabled'

    def update(self):
        # self.sound_button.on = self.data_dic['sound']
        pass

    def leave(self):
        # self.data_dic['sound'] = self.sound_button.on
        pass

    def draw(self):
        # self.window.fill('blue')
        self.window.fill('turquoise3')
        self.screen_mgr.draw()


if (__name__ == '__main__'):
    from Helpers import window_init, loop

    window_size = (c('width_window'), c('height_window'))
    window = window_init(size=window_size, color='red')
    scores = HighScores(window)

    loop()


"""
pygame.quit()
quit()
"""
