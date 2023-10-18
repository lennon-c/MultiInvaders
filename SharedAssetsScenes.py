# -*- coding: utf-8 -*-
"""
Created on Sun Mar 19 16:55:01 2023

@author: carol

For the future, dont set class attributes within functions.
It turned out to be very difficult and debbug to read.

"""

import pygame
import os
from Scenes import Scene as SceneBase
from Constants import c
from Assets import Asset, Text, ButtonImage, Pane, Square, Circle, ButtonImageActivate, PaneImage, PaneSurface
from HighScores import ScoresData
from datetime import datetime
from babel.dates import format_timedelta
from UserSettings import UserSetting

# class used for play assets 
class Variant(PaneSurface):
    """Add a status 'selected' that defines the background and surfaces to be shown depending on wether 'selected' is True or False."""

    def __init__(self, window, border_radius=None, surfaces=None, colors=None):
        super().__init__(
            window, surfaces['on'], color=colors['on'], border_radius=border_radius)
        self.surfaces = surfaces
        self.colors = colors
        self._selected = True

    @property
    def selected(self):
        return self._selected

    @selected.setter
    def selected(self, state):
        if state == True:
            self.surface = self.surfaces['on']
            self.color = self.colors['on']
        else:
            self.surface = self.surfaces['off']
            self.color = self.colors['off']

        self._selected = state


class Scene(SceneBase):
    """Assets that are accesed by all scences are designed here."""

    # CONSTANTS
    border_radius = c('border_radius')
    fontsize_small = c('fontsize_small')
    fontsize_medium = c('fontsize_medium')
    fontsize_large = c('fontsize_large')
    images_path = c('images_path')
    text_options = {'fontname': c('fontname')}
    score_data = ScoresData()
    user = UserSetting()
    data_dic = user.settings

    def __init__(self, window):
        self.window = window

    def images_files(self, name):
        """Return images file dictionary for the construction of image buttons."""
        colors = {'default': 'red', 'hover': 'blue', 'pressed': 'green', 'disabled': 'grey'
                  }

        def file(name, color): return f'{color}_{name}.svg'
        files = {key: file(name, color) for key, color in colors.items()}
        return files

    def shared_assets(self, bubble):
        """Set Assets that are common across Scenes. Nomarlly called when the scene is initiated."""
        # it is used in several scenes and not necessarily with the same format.
        def buttons_set(container):
            color = 'cyan'  # grey81 #  turq = 102, 228,255
            grid = Square(container, '', (10, 20), color=color,
                          border_radius=self.border_radius)

            play_button = ButtonImage(container, self.images_path, self.images_files(
                'play'), resize=(60, 60), enter_activated=True)
            home_button = ButtonImage(
                grid, self.images_path, self.images_files('home'), resize=(50, 50))
            sound_button = ButtonImageActivate(grid, self.images_path, self.images_files(
                'sound'), self.images_files('silence'), resize=(55, 45))
            sound_button.on = self.data_dic['sound']

            history_button = ButtonImage(
                grid, self.images_path, self.images_files('history'), resize=(40, 49))

            Asset.grid(1, 4, grid,  [
                       play_button, home_button, history_button, sound_button], margin=25, outer_margin=20)

            for i in play_button, home_button, sound_button, history_button:
                i.align('centery')

            return grid, play_button, home_button, sound_button, history_button

        self.bub_buttons, self.start_button, self.home_button, self.sound_button, self.history_button = buttons_set(
            bubble)
        assets = self.bub_buttons, self.start_button, self.home_button, self.sound_button, self.history_button

        return assets

    def intro_assets(self, bubble):
        """Set of assets for intro Scene, called when Intro is initiated."""
        def title_text(bubble,text):
            # small title within selection bubbles
            title = Square(bubble,  text
                                 , size = (157 + 20 , 23 + 20)
                                 # , color = 'green'
                                 , color = c('palette')[3]
                                , fontsize = self.fontsize_small
                                , fontcolor = 'red'
                                # , fontcolor = c('palette')[1]
                                , fontname = c('fontname')
                                , border_radius = 30
                                , margin = 2)
            return title


        def choose_numbers(container):
            # white bubble
            bubble = Square(container, '', (10,10), 'white', border_radius = self.border_radius)
            grid = Pane(bubble, (10,10))

            squares = dict()
            for n in list(range(1,16)):
                squares[n] = Square(grid,  n, (40, 40)
                                    , color = 'yellow'
                                    , fontname = c('fontname'), fontsize = self.fontsize_medium
                                    , border_radius = self.border_radius)
                # set selected at start
                if n in self.data_dic['selected_numbers']:
                    squares[n].selected = True

            Asset.grid(5,3, grid, squares.values(), margin=5)

            text = title_text(bubble, 'Choose your numbers')
            Asset.grid(2,1,bubble,  [ text, grid  ]  ,  margin=10, outer_margin = 10)
            grid.align('centerx')
            text.align('centerx')

            assets = [bubble, text ] +  list(squares.values())
            return bubble, assets, squares


        def choose_speed(container  ):
            bubble = Square(container, '', (10,20), 'white', border_radius = self.border_radius)
            grid = Pane(bubble, (10,20))

            levels = dict()
            for level  in ['normal', 'fast', 'even faster']:
                levels[level] = Square(grid,  level, (120, 40)
                                        , color = 'yellow'
                                        , fontname = c('fontname'), fontsize = self.fontsize_medium
                                        , border_radius = self.border_radius)

                if level == self.data_dic['selected_speed'] :
                    levels[level].selected = True
                else:
                    levels[level].selected = False


            Asset.grid(3, 1, grid, levels.values(), margin=10  )

            text = title_text(bubble, 'Choose your speed')
            Asset.grid(2,1, bubble,  [ text, grid  ]  ,  margin=10, outer_margin = 10)
            grid.align('centerx')
            text.align('centerx')
            assets = [bubble, text ] +  list(levels.values())
            return bubble, assets, levels

        def choose_avatar(container ):
            bubble  = Square(container, '', (10,20), 'white', border_radius = self.border_radius)
            grid  = Pane(bubble, (10,20))

            avatars = dict()
            size = (60,60)
            for n in list(range(0,10)):
                # if n!=4: # drop pig
                _file =  os.path.join(self.images_path, f'{n}_avatar.svg')
                avatars[n] = PaneImage(grid, size, _file, 'white',  border_radius = 20  )
                if _file == self.data_dic['selected_avatar']:
                    avatars[n].selected = True
                else:
                    avatars[n].selected = False

                # avatars[n].color = 'yellow' if n== 0  else 'white'

            Asset.grid(5,2, grid, avatars.values(), margin=5)

            text = title_text(bubble, 'Choose your avatar')
            Asset.grid(2,1, bubble,  [ text, grid  ], margin=  10, outer_margin = 10)

            grid.align('centerx')
            text.align('centerx')

            assets = [bubble, text ] +  list(avatars.values())

            return bubble, assets, avatars

        def choose_game(container):
            # main container
            bubble = Square(container, '', (10,20), 'white', border_radius = self.border_radius)
            grid = Pane(bubble, (10,20))

            # letters
            def letter(grid, text):
                color = 'white'
                if text == '?' :
                    color = 'cyan'
                letter_text = Square(grid,  text, (25, 25)
                                        , color = color
                                        , fontname = c('fontname')
                                        , fontsize = self.fontsize_medium
                                        , border_radius = self.border_radius)
                return letter_text

            # games
            def level(text, container):

                game =  Pane(bubble, (10,20))
                # get each letter into a square
                game_list =  [letter(game, l) for l  in  list(text)]
                # allign letters
                Asset.grid(1, len(game_list), game, game_list, margin=0, outer_margin =10  )
                for l in game_list:
                    l.draw()

                pygame.Surface.set_colorkey(game.surface, 'white')
                game = PaneSurface(bubble,game.surface, border_radius = self.border_radius)

                return game

            game1 = level('1x2=?', bubble)
            game2 = level('?x?=2', bubble)

            Asset.grid(2, 1, grid, (game1,game2), margin=10  )

            # title
            text = title_text(bubble, 'Choose your game')
            Asset.grid(2,1, bubble,  [ text, grid  ]  ,  margin=10, outer_margin = 10)

            grid.align('centerx')
            text.align('centerx')

            levels = {1: game1, 2:game2}

            # # assign selection status
            for n, game in levels.items():
                if self.data_dic['selected_game']  == n:
                    game.selected = True
                else:
                    game.selected = False

            assets = [bubble, text] +  list(levels.values())
            return bubble, assets, levels

        def title_pane(container):
            """Set main title of the game."""
            print(c('palette')[2])
            print(c('palette') )
            bubble  = Square(container, '', (10,10), c('palette')[2], border_radius = self.border_radius) # paleturquoise1 'olivedrab2'
            # deeppink darkorange
            display = pygame.display.get_surface()
            w, h = display.get_size()

            title = Text( bubble , 'Multi Space Invaders'
                             , h_align =1 , v_align=1
                             , width = w*0.95 , height = 1, margin =  1
                             , wrap = False, adjust_size = True
                             , fontsize = self.fontsize_large
                               , fontcolor = 'red'
                               # , fontcolor = c('palette')[1]
                             , **self.text_options)

            bubble.include_aligned(title, margin =5, adjust_size = True)
            assets =  bubble, title
            return assets

        #### run functions
        # selections
        all_assets = list()
        self.bub_numbers , assets, self.squares = choose_numbers(bubble)
        all_assets = all_assets + assets
        self.bub_speed , assets, self.speeds = choose_speed(bubble)
        all_assets = all_assets + assets
        self.bub_avatars, assets, self.avatars = choose_avatar(bubble)
        all_assets = all_assets + assets

        self.bub_games, assets, self.games = choose_game(bubble)
        all_assets = all_assets + assets

        assets = title_pane(self.window)
        self.bub_title, title   = assets

        all_assets = all_assets + list(assets)

        return all_assets


    def play_assets(self):
        """Set of assets for Play Scene, called when Play is initiated."""
        def score_pane(big_bubble, bub_text , image_size  ):
            # here I do not know yet which is the image to show

            w,h = self.window.get_size()
            avatar = Pane(big_bubble, image_size)
            # print(w/2)

            size = Text(bub_text , f'Last answer:{chr(10)}15 x 15 = 225'
                         , h_align =0, v_align=1
                         , margin =  0
                         , fontsize = self.fontsize_small
                         , fontcolor = 'blue'
                         , color = bub_text.color
                         , wrap = False, adjust_size = False
                         , **self.text_options )

            print(size.surface.get_size() )
            print(size.line_h)
            print(size.text_surface.get_size() )
            w,h =size.surface.get_size()

            score_text= Text(bub_text , ''
                         , h_align =1, v_align=1
                          , margin =  0
                         , height = size.line_h*3
                         , fontsize = self.fontsize_small
                         , fontcolor = 'blue'
                         , color = bub_text.color
                         , wrap = False, adjust_size = False
                         , **self.text_options )

            last_answer = Text(bub_text , ''
                         , h_align =1, v_align=1
                          , margin =  0
                         , width = w
                         , height = size.line_h*3
                         , fontsize = self.fontsize_small
                         , fontcolor = 'blue'
                         , color = bub_text.color
                         , wrap = False, adjust_size = False
                         , **self.text_options )

            return  avatar, score_text, last_answer


        def mat(bottom, top):
            """ Frame and board for the game, it adjusts to the possition of top and bottom panels"""
            # only the frame is drwan in the game
            # yellow
            frame = Pane(self.window,self.window.get_size() , c('palette')[1])

            w = c('width_mat')
            h = c('height_window') - bottom.rect.height  - top.rect.height

            # board is used to get the size of the playing board
            board = Pane(self.window, (w, h), color = 'black')
            board.rect.y = top.rect.bottom
            board.align('centerx')

            # make transparent the board area on the frame
            pygame.draw.rect(frame.surface, 'black', board.rect, border_radius = self.border_radius)
            pygame.Surface.set_colorkey(frame.surface, 'black')

            return frame, board


        def middle(board):
            w, h = board.rect.size
            middle_text = Text(self.window , 'Press play or ENTER to start playing...'
                                    , adjust_size = True
                                    , width = w*0.85 , height = h*0.7
                                    , fontcolor = 'blue'
                                    , **self.text_options)
            return middle_text


        def game_variants(circles_on_color, circles_off_color, background_on, background_off, pos):
            """
            create the dices for the game variants

            Parameters
            ----------

            circles_on_color = color of small circles when activated
            circles_off_color = color of small circles when desactivated
            background_on = background color when activated
            background_off = background color when activated
            pos:  list of positions ['centery', 'bottom', 'top']

            """

            # create surface
            surface_on = pygame.Surface((42,42))
            surface_on.convert_alpha
            surface_on.fill('white')
            pygame.Surface.set_colorkey(surface_on, 'white')

            surface_off = surface_on.copy()

            circles_on = list()
            circles_off = list()
            for n in range(3):
                c =  Circle(surface_on , '' , fontsize = 1 , size=  (10,10) , color = circles_on_color)
                circles_on.append(c)
                c =  Circle(surface_off , '' , fontsize = 1 , size=  (10,10) , color = circles_off_color)
                circles_off.append(c)

            # align horizonal
            Asset.grid(1, 3, surface_on, circles_on, margin = 2, outer_margin= 2)
            Asset.grid(1, 3, surface_off, circles_off, margin = 2, outer_margin= 2)

            # align veritical
            for circle, pos in zip( circles_on + circles_off , pos*2) :
                circle.align( pos, margin = 5)

            # print circles into their own surfaces
            for circle in  circles_on + circles_off:
                circle.draw()

            surfaces = {'on' : surface_on
                        , 'off' : surface_off}

            colors = {'on' : background_on
                        , 'off' : background_off }

            # get windows display
            screen = pygame.display.get_surface()
            variant =   Variant(screen, border_radius = 15, surfaces = surfaces, colors = colors )

            return variant

        def choose_variant( container  ):
            circles_on_color =  'red'  # 'orange'
            circles_off_color = 'gray65'
            background_on =   c('palette')[4] # 'yellow'
            background_off =    'gray92'

            bubble  = Square(self.window ,'', (10,20), color = 'white' , border_radius =self.border_radius)

            # variant 1
            pos = ['centery']*3
            variant_1 =  game_variants(circles_on_color ,circles_off_color, background_on, background_off, pos )

            # variant 2
            pos = ['centery', 'bottom', 'top']
            variant_2 =  game_variants(circles_on_color ,circles_off_color, background_on, background_off, pos)

            levels = {'variant_1': variant_1
                      ,'variant_2' : variant_2 }
            
            for level, obj in levels.items():
                if level == self.data_dic['selected_variant']:
                    obj.selected = True 
                else:
                    obj.selected = False 

            Asset.grid(1, 2 , bubble,  levels.values() , margin=10, outer_margin= 10)

            for i in  variant_1, variant_2:
                i.align('centery')


            return bubble, levels


        #### Assets to object
        #### BOTTOM
        # bub buttons and buttons
        # self.bub_buttons, self.start_button, self.home_button, self.sound_button, self.history_button
        buttons = list(self.shared_assets(self.window)) # windows does not matter here as the window of reference will change
        self.bub_variants , self.variants = choose_variant(self.bub_buttons)
        buttons = buttons[1:]
        buttons.insert(1, self.bub_variants )
        Asset.grid(1,len(buttons), self.bub_buttons ,  buttons ,  margin=  20,   outer_margin = 20)

        for button in buttons:
            button.align(align = 'centery')
        self.bub_buttons.align(align = 'midbottom')


        #### TOP
        # orange
        self.top = Square(self.window, '', (10,10) , c('palette')[2], border_radius = self.border_radius)

        self.bub_text = Square(self.top, '', (10,10) , 'cyan', border_radius = self.border_radius)
        self.avatar_img, self.score_text,  self.last_answer=  score_pane(self.top ,self.bub_text ,  c('avatar_play_size'))

        Asset.grid(1,2, self.bub_text,  [ self.score_text, self.last_answer ]  ,  margin=10  ,   outer_margin = 10)
        self.score_text.align('centery')
        self.last_answer.align('centery')

        Asset.grid(1,2, self.top,  [ self.avatar_img , self.bub_text  ]  ,  margin=  10 ,   outer_margin = 5)


        #### MAT and BOARD
        self.frame, self.board = mat(self.bub_buttons, self.top) # create a frame and board area

        self.top.rect.x =  self.board.rect.x
        self.bub_buttons.rect.right =  self.board.rect.right
        # self.top.align(align = 'midtop')
        self.bub_text.align('centery')
        self.avatar_img.align('centery')


        #### MIDDLE TEXT
        self.middle_text = middle(self.board) # text for introduction
        self.middle_text.align('center')


        #### ASSETS
        # self.top_panel, self.bub_variants , self.variants,  self.bubble
        all_assets =  [self.frame
                       , self.middle_text
                       , self.top
                       , self.bub_text
                       , self.bub_buttons
                       , self.bub_variants ]
        all_assets  = all_assets +  buttons # buttons
        all_assets =( all_assets
                    + [self.avatar_img, self.last_answer, self.score_text ]
                    + list(self.variants.values()) )

        return all_assets

    def scores_assets(self):
        """Set of assets for HighScores Scene, called when HighScores is initiated."""
        today = datetime.now()

        def text_date(date, width = 10):
            text = Text( self.window , date
                         , h_align =0, v_align=1
                         , margin =  1
                         , fontsize = self.fontsize_medium
                         , fontcolor = 'blue'
                         , color = None
                         , width = width
                         , wrap = True, adjust_size = True
                         , **self.text_options )
            return text

        def text_score(score):
            text = Square(self.window,  score, (40, 40)
                                    , color = 'yellow'
                                    , fontname = c('fontname'), fontsize = self.fontsize_medium
                                    , border_radius = self.border_radius)
            return text

        def text_title(string):
            text = Square(self.window,  string, (50 , 40 )
                                    , color = 'cyan'
                                    , fontcolor ='red'
                                    , fontname = c('fontname'), fontsize = self.fontsize_medium
                                    , border_radius = self.border_radius)
            return text

        container_big = Square(self.window,'', (10,20), color = 'green' , border_radius = self.border_radius )
        container  = Square(self.window,'', (10,20), color = 'white' , border_radius = self.border_radius )
        assets = [container_big, container]

        # if list of highest scores is not empty
        if len(self.score_data.scores_list)>0 :

            container_score = Square(self.window,'', (10,20), color = 'white' , border_radius = self.border_radius )
            assets = assets + [  container_score]

            scores_lst = list()
            for score in self.score_data.scores_list :
                _list = list()
                # score
                _list.append(text_score(str(score[0])))
                # image
                _list.append(PaneImage(self.window, (40,40), score[1]) )
                # date
                date = datetime.fromisoformat(score[2])
                delta = date -today
                date_text = format_timedelta(delta, granularity='second', threshold=1, locale='en_US', add_direction=True)
                _list.append(text_date(date_text))
                scores_lst.append(_list)

            # a grid for each score
            grids = [Pane(self.window, (10,10)) for i in scores_lst ]
            assets = assets +  grids
            for n,score in enumerate(scores_lst) :
                cols = len(score) # items to print per score
                Asset.grid(1,cols, grids[n] , score ,  margin=  30,   outer_margin = 0)
                assets = assets + score

            # Asset.grid( len(grids)//2, 2,  container,  grids ,   margin=  5,   outer_margin = 5)
            Asset.grid( len(grids) , 1, container_score,  grids ,   margin=  5,   outer_margin = 10)

            bub_title  = Square(self.window,'', ( 10 ,10), color = 'cyan' , border_radius = self.border_radius )
            assets = assets + [bub_title]

            headings = list()
            for t in 'score', 'player', 'date':
                headings.append(text_title(t))

            assets = assets   +  headings

            Asset.grid( 1 , len(headings), bub_title,  headings, margin=  30, outer_margin = 10)
            Asset.grid( 2 , 1,  container ,  [ bub_title, container_score ],  margin=  0,   outer_margin = 5)

            h = bub_title.rect.height
            w = container.rect.width
            bub_title.rect = *container.rect.topleft, w, h

        else: # if not yet scores in list
            no_score_text = Text(container  , "No scores yet!\nStart playing..."
                         , h_align =1, v_align=1
                         , margin =  3
                         , fontsize = self.fontsize_medium
                         , fontcolor = 'blue'
                         , color = None
                         ,  width = 200
                         , wrap = True, adjust_size = True
                         , **self.text_options )

            container.include_aligned(no_score_text, adjust_size  = True)
            assets = assets + [no_score_text]

        # bring buttons
        bub_buttons, *buttons  = self.shared_assets(self.window)

        self.garbage_button =  ButtonImage(bub_buttons, self.images_path, self.images_files('garbage'), resize=(40,49))
        buttons = list(buttons)
        buttons.append(self.garbage_button )

        Asset.grid( len(buttons)  , 1,  bub_buttons ,  buttons   ,   margin=  30,   outer_margin = 10)
        for button in buttons:
            button.align('centerx')
        assets = assets + [bub_buttons] +  buttons
        Asset.grid( 1 , 2,  container_big ,  [ container, bub_buttons ],   margin=  20,   outer_margin = 20)
        container_big.align('center')
        return assets

    def shared_handle(self, event):
        """Handle of pygame events used in all Scenes."""
        if self.sound_button.handle(event):
            self.sound_button.on = not self.sound_button.on
            self.data_dic['sound'] = self.sound_button.on

        # add history button
        if self.history_button.handle(event) and self.id != 'scores' :
            self.go_to('scores' )
