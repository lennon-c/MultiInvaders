# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 14:02:47 2023

@author: carol
"""

import pygame
from pygame.locals import (
    MOUSEBUTTONDOWN,  MOUSEMOTION, MOUSEBUTTONUP, SRCALPHA)
from textwrap import wrap
import string
import random
from os import path
from copy import deepcopy
from itertools import product
import math
from lorem_text import lorem

class Display():
    """For conveneace assets can be created relative to a small surface different from the final display surface.

    But after their construction is finished, their respective rects have to be adjusted to reflect the position of the asset in the final display surface. This adjustment is conducted here.

    Only Assets can be managed, pygame surfaces have to be blitted or transformed manually into assets to be included.
    """

    def __init__(self, display,  *assets  ):
        self.display = display
        self.set_initial(*assets)
        self.previous_placement(*assets) # maybe not necessary here
        self._assets = list(assets) # create problems with comparisons

    def __del__(self):
        # print("Inside __del__")
        for asset in self._assets:
            # back to original values
            asset.rect = asset.rect_initial.copy()
            # delete traces
            del asset.rect_initial
            del asset.rect_0

    @property
    def assets(self):
        return self._assets

    @assets.setter
    def assets(self, assets):

        assets = list(assets)
        new_assets = list()
        for asset in assets:
            if asset not in self._assets:
                new_assets.append(asset)

        # print(f'{new_assets=}')
        self.set_initial(*new_assets)
        self.previous_placement(*new_assets)

        # deleted assets, returning to original
        for asset in self._assets:
            if asset not in assets:
                # print('deleting asset')
                # back to original values
                asset.rect = asset.rect_initial.copy()
                # delete traces
                del asset.rect_initial
                del asset.rect_0

        self._assets = assets

    # for initiating the class and adding new assets to the list
    def set_initial(self, *assets):
        for asset in assets:
            asset.rect_initial = asset.rect.copy()

    # for updating
    def previous_placement(self, *assets):
        for asset in assets:
            asset.rect_0 = asset.rect.copy()

    def new_placement(self, asset):
        current = asset.window
        x = asset.rect_0.x
        y = asset.rect_0.y

        while current != self.display:
            # look at the rect of the canvas
            try: # if already in assets
                parent_x0 = current.rect_0.x
                parent_y0 = current.rect_0.y
            except: # if not included in assets
                parent_x0 = current.rect.x
                parent_y0 = current.rect.y

            x = parent_x0 + x
            y = parent_y0 + y
            current = current.window
        return x,y

    def set_new_placement(self, asset):
        asset.rect.topleft = self.new_placement(asset)

    def update(self):
        # reset base location and window
        self.previous_placement()

        for asset in self.assets:
            self.set_new_placement(asset)

    def draw(self):
        for asset in self.assets:
            asset.draw(canvas = self.display)


class Asset():
    """Set attributes of visible and enabled that can be used to modify the way assets are drawn and behave.

    Assets must have at least a rect and a surface. These attributes will be used for drawing and handling the asset.
    """

    # @abstractmethod
    def __init__(self, window):
        self.window = window
        self.visible = True
        self.enabled = True
        self._rect = pygame.Rect(0, 0, 0, 0)
        self._surface = pygame.Surface((0, 0), SRCALPHA)
        self._original = pygame.Surface((0, 0))
        super().__init__()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, dimension):

        topleft = dimension[:2]
        size =  dimension[-2:]

        if size != self._rect.size:
           self._surface =  pygame.transform.smoothscale(self.original,  size)

        self._rect.topleft =  topleft
        self._rect.size =  size

    @property
    def surface(self):
        return self._surface

    @surface.setter
    def surface(self, layer):
        size = layer.get_size()
        self._surface =  layer
        self._original = layer.copy() # transformations use original
        topleft = self._rect.topleft
        self._rect  = pygame.Rect( *topleft, *size)

    @property
    def original(self):
        return self._original

    def enable(self):
        """Set this widget enabled."""
        self.enabled = True

    def disable(self):
        """Disables the current widget."""
        self.enabled = False

    def hovering(self, event_pos):
        """
        Return true if mouse hovering the surface (focus)
        # this method can be overwritten if necessary by the subclasses
        """
        if not self.enabled or not self.visible:
            return False

        return self.rect.collidepoint(event_pos)

    def draw(self, x = None , y = None, canvas = None):
        """
        draw and update location of the container of the text image
        """
        if not self.visible:
            return

        if x is None:
            x = self.rect.x
        else :
            self.rect.x  = x

        if y is None:
            y = self.rect.y
        else:
            self.rect.y  = y

        if canvas is None:
            canvas = self.window

        try: # if sub class has some special drawings
            self._draw_tweaks(x,y,canvas)

        except: #
            if isinstance(canvas, Asset):
                canvas.surface.blit(self.surface, (x,y))

            else: # canvas is a pygame surface object, such as the main display
                canvas.blit(self.surface, (x,y))


    def align(self, align = None, margin = 0 , h_align = 1, v_align = 1 ):
        """Set aligned the Asset object within other asset object or within a pygame surface.

        Parameters:
        align (string) = top, left, bottom, right, topleft, bottomleft, topright, bottomright
        , midtop, midleft, midbottom, midright, center, centerx, centery.

        """
        pos = dict(top=[None, 0], left=[0, None], bottom=[None, 2], right=[2, None], topleft=[0, 0], bottomleft=[0, 2], topright=[2, 0], bottomright=[2, 2], midtop=[1, 0], midleft=[0, 1], midbottom=[1, 2], midright=[2, 1], center=[1, 1], centerx=[1, None], centery=[None, 1]
                   )

        if align is not None:
            try:
                h_align, v_align = pos[align]

            except:
                print(f'Entry not found, allowed arguments:{chr(10)}{ ", ".join(list(pos.keys()))}')
                return

        w, h =  self.surface.get_size()

        if isinstance(self.window, Asset):
            w0 = self.window.rect.width
            h0 = self.window.rect.height
        else :
            w0 = self.window.get_width()
            h0 = self.window.get_height()

        if h_align is not None:
            # set location within the container box
            x = 0
            x = (0 + margin , (w0-w)//2 , (w0 - w - margin ))[h_align] + x
            self.rect.x = x
        if v_align is not None:
            y = 0
            y = (0 + margin , (h0-h)//2 , (h0 - h - margin ))[v_align] + y
            self.rect.y =  y


    def include_aligned(self,  other , margin = 0, h_align = 1, v_align = 1,  adjust_size  = False):
        """Set the position of another object (other) aligned inside the object Asset (self).

        The other object can be either another Asset or a pygame Surface object.
        It returns the x,y of the other object relative to Asset object
        If other is an Asset, then its x,y will be adjusted.
        """
        if isinstance(other, Asset):
            w, h =  other.surface.get_size() # image to paste
        else: # any surface
            w, h =  other.get_size()

        x = 0
        y = 0

        width, height =  self.surface.get_size() # destination surface

        if adjust_size:
            # width
            w0 =  width if  width> (w  +  2 * margin ) else (w  +  2 * margin )
            # height
            h0 =  height if  height> (h + 2 * margin ) else (h +  2 * margin )

            # size adjusted
            self.rect  = (0, 0 , w0, h0)

        else:
            w0 = width
            h0 = height

        if self.color is not None:
            self.surface.fill(self.color )

        # set location within the container box
        x = (0 + margin , (w0-w)//2 , (w0 - w - margin ))[h_align]
        y = (0 + margin , (h0-h)//2 , (h0 - h - margin ))[v_align]

        if isinstance(other, Asset):
            # update position if it is an assets
            other.rect.x = x
            other.rect.y = y

        # else :
        #     print('sub_surface is not Asset object')
        #     print(sub_surface)

        # return info to modify if necessary sub_surface position
        return   x,y

    @staticmethod
    def grid( nrows, ncols , container, objects, margin = 0 , outer_margin = 0 , adjust_size_grid = True):
        """
        Position objects in a grid of 'nrows' and 'ncols' with coordinates relative to the container surface.
        Only for Asset objects. if the container is also an asset, coordinates of the container are set to topleft and size is adjusted to set the elements. If container is not an asset, then its size is not adjusted

        """
        # rows and cols dic
        row_h = {row : 0 for row in range(nrows)}
        col_w = {col : 0 for col in range(ncols)}

        # find max of objects' height per row and the max width of objects per column
        for  obj,  ( r, c)   in  zip(objects, product(range(nrows), range(ncols))):
            #  row_h[r] is updated with the max height found across the objs of the row (across columns)
            #  col_w[c] is updated with the max width found across the objs of the col (across rows)
            w,h = obj.rect.size
            row_h[r] =  h if h > row_h[r]  else row_h[r]
            col_w[c] =  w if w > col_w[c]  else col_w[c]


        x = 0 + outer_margin
        y = 0 + outer_margin
        _height = 0
        _width = 0
        max_bottom = 0
        max_right = 0

        for  obj,  ( r, c)   in  zip(objects, product(  range(nrows), range(ncols))):
            # print( 'rows',r, 'columns', c)
            obj.window = container # change display of reference

            # 3 mutually exclusive cases
            if nrows!=1 and ncols!=1:
                y = (row_h[r] + margin) * r  # based on the max height for the row r and its position on the column (r)
                x = (col_w[c] + margin) * c  # based on the max width for the col c and on the position on row (c)
            elif nrows==1:
                x = x + _width # notice that in this case y is assigned before the loop
                _width =  obj.rect.width + margin
            else: # only one column
                y = y + _height # notice that x is assigned before the loop
                _height = obj.rect.height + margin

            # assign corrected coordinates to objetcs
            obj.rect.topleft = x,y

            # find most right x and most bottom y to define the width and height of the container
            if c == (ncols - 1 ): # objs of the last column
                # find the rightest most x coordinate of the container
                _max = x + col_w[c]  + outer_margin
                max_right = _max if _max > max_right else max_right

            if r == (nrows - 1) : # objs of the last row
                # find the bottom y coordinate of the container
                _max = y + row_h[r] + outer_margin
                max_bottom = _max if _max > max_bottom else max_bottom

        if adjust_size_grid:
            try:
                left, top = container.rect.topleft
                container.rect =left, top , max_right, max_bottom # change size of conteiner
            except:
                print('conteiner not an asset ')


class Pane(Asset):
    """Initiate the minimun expression of an asset, just a box."""

    def __init__(self, window, size, color = None ):
        super().__init__(window)

        self.rect = (0,0, *size)
        self.surface = pygame.Surface(size,   SRCALPHA)
        if color is not None:
            self.surface.fill(color)
        self.color = color
        self.enabled = True

class PaneSurface(Pane):
    """Allow creating a square with defined surface"""
    def __init__(self, window, surface, color = None, border_radius = 0 ):
        size = surface.get_size()
        super().__init__(window, size, color )
        self.border_radius  = border_radius
        self.surface = surface


    def _draw_tweaks(self, x,y,canvas):
        """To include when the draw method of the Asset class is invoked.

        Modify to include the desired shape.
        """
        try:
            container = canvas.surface
        except: # canvas is a pygame surface object, such as the main display
            container = canvas

        if self.color is not None:
            pygame.draw.rect(container, self.color, self.rect
                             , width= 0
                             , border_radius= self.border_radius )
        container.blit(self.surface, self.surface.get_rect(center = self.rect.center))

class PaneImage(Pane):
    """Allow creating a square with an image."""
    def __init__(self, window, size, file, color = None, border_radius = 0 ):
        super().__init__(window, size, color )
        self.border_radius  = border_radius
        self.file = file
        self.surface = self.get_image()

    # Here I could implement a setter getter of file
    # setter, => update surface

    def get_image(self):
        img = pygame.image.load(self.file)
        size = img.get_size()
        if size != self._rect.size:
            img = pygame.transform.smoothscale(img , self._rect.size)
        return img

    def _draw_tweaks(self, x,y,canvas):
        """
        To include when the draw method of the Asset class is invoked
        Modify to include the desired shape
        """
        try:
            container = canvas.surface
        except: # canvas is a pygame surface object, such as the main display
            container = canvas

        if self.color is not None:
            pygame.draw.rect(container, self.color, self.rect
                             , width= 0
                             , border_radius= self.border_radius )
        container.blit(self.surface, self.surface.get_rect(center = self.rect.center))


class ShapedText(Asset):
    """ lighter version of Text. To be used as pattern to write a centered text into a geometric shape
    As it is, it draws a rectable, by modifying the draw_tweaks, it can be used to draw other shapes.
    """

    defaults = dict(
                    # text options
                      antialias = True
                    , fontcolor = 'black'
                    , fontname = 'comicsansms'
                    , fontsize = 24
                    , bold= False
                    , italic= False

                    )

    def __init__(self, window,  text, size, color, defaults, **options):
    # def __init__(self, window,  text, size, color,  defaults, **options):
        super().__init__(window)

        self.options = self.defaults.copy()
        self.options.update(defaults) # coming from shape

        kwargs = dict()
        for key, value in self.options.items():
            # only keywords defined in defaults are passed as attribute, otherwise they are ignored
            kwargs[key] = options.get(key, self.options.get(key, f'Problem with {key}. Very unlikely to happen'))

        self.__dict__.update(kwargs)
        self.rect = (0,0, *size) # this resizes the surface as well
        self.color = color
        self.font = pygame.font.SysFont( self.fontname , self.fontsize
                                        , bold=self.bold, italic=self.italic)

        self.text = text
        self.moving = False
        self.selected = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text_image = None
        self._text = text

    @property
    def text_image(self):
        if self._text_image is None:
            self._text_image = self.font.render(str(self.text)
                                                , self.antialias
                                                , self.fontcolor
                                                # , self.color
                                                )

            self._text_image.convert_alpha()
            size_img = self._text_image.get_size()
            size_rect = self.rect.size
            topleft = self._rect.topleft

            if  any( i > j for i,j in zip(size_img, size_rect)):
                if size_rect[0] == size_rect[1]:
                    print(f'Adjust size to {max(*size_img)} !!!')
                    # self.rect = (*topleft, max(*size_img), max(*size_img))

                else:
                    new_size = [max(i,j) for i,j in zip(size_img, size_rect)]
                    print(f'Adjust size to  {new_size} !!!')
                    # self.rect = (*topleft, *new_size)

        return self._text_image


    def _draw_tweaks(self, x,y,canvas):
        """
        EXAMPLE
        To include when the draw method of the Asset class is invoked
        Modify to include the desired shape
        """
        try:
            container = canvas.surface
        except: # canvas is a pygame surface object, such as the main display
            container = canvas

        pygame.draw.rect(container, self.color, self.rect
                         , width= 0)
        container.blit(self.text_image, self.text_image.get_rect(center = self.rect.center))




class Square(ShapedText):
    """ lighter version of text. Whrite a centered text in a square or rectangle
    # this actually allows rect"""
    def __init__(self, window, text, size, color, **options ):

        defaults = dict(width=0, border_radius=0, border_top_left_radius=-1,
                        border_top_right_radius=-1, border_bottom_left_radius=-1
                        , border_bottom_right_radius=-1
                        )

        super().__init__(window, text, size, color, defaults, **options )


    def _draw_tweaks(self, x,y,canvas):
        """
        To include when the draw method of the Asset class is invoked
        Modify to include the desired shape
        """
        try:
            container = canvas.surface
        except: # canvas is a pygame surface object, such as the main display
            container = canvas

        pygame.draw.rect(container, self.color, self.rect
                         , width= self.width
                         , border_radius= self.border_radius
                         , border_top_left_radius= self.border_top_left_radius
                         , border_top_right_radius= self.border_top_right_radius
                         , border_bottom_left_radius= self.border_bottom_left_radius
                         , border_bottom_right_radius= self.border_bottom_right_radius)
        container.blit(self.text_image, self.text_image.get_rect(center = self.rect.center))

class Circle(ShapedText):
    def __init__(self, window, text, size, color, **options ):
        defaults = dict(width=0, draw_top_right=True, draw_top_left=True
                        , draw_bottom_left=True, draw_bottom_right=True)
        super().__init__(window, text, size, color, defaults,  **options )

    @property
    def radius(self):
        return self.rect.width//2

    def _draw_tweaks(self, x,y,canvas):
        """
        To include when the draw method of the Asset class is invoked
        Modify to include the desired shape
        """
        try:
            container = canvas.surface
        except: # canvas is a pygame surface object, such as the main display
            container = canvas

        # print(container, self.color, self.rect.center, self.radius)
        pygame.draw.circle(container, self.color, self.rect.center, self.radius
                            , width = self.width , draw_top_right=self.draw_top_right
                            , draw_top_left=self.draw_top_left
                            , draw_bottom_left=self.draw_bottom_left
                            , draw_bottom_right=self.draw_bottom_right)

        container.blit(self.text_image, self.text_image.get_rect(center = self.rect.center))

    def hovering(self, event_pos):
        """
        Return true if mouse hovering the surface
        """
        distance = math.sqrt(((event_pos[0] - self.rect.center[0]) ** 2) +
                                 ((event_pos[1] - self.rect.center[1]) ** 2))

        if distance <= self.radius:
            # print('hovering')
            return True
        else:
            # print('outside')
            return False

    def collide(self, asset):
        """
        Return true if the circle collides another rectangle of an asset
        """
        rect = asset.rect
        locations = [ rect.topleft, rect.bottomleft, rect.topright, rect.bottomright
                      , rect.midtop, rect.midleft, rect.midbottom, rect.midright]

        for loc in locations:

            distance = math.sqrt(((loc[0]  - self.rect.center[0]) ** 2) +
                                     ((loc[1]  - self.rect.center[1]) ** 2))

            if distance <= self.radius:
                # print('hovering')
                return True

        return False


class TextAssets(Asset):
    """Create a text surface image.

    This is not meant to be accessed directly. Needs lots of improvements.
    """
    min_wrap_width = 15

    def __init__(self, window, text='Text',  **options):
        """Instantiate and render the text object."""
        super().__init__(window)

        # Set instance attributes of the passed options arguments, or in their absence their defaults values
        passed_args = self._defaults()

        for k in options:  # overwrite defaults
            if k in passed_args:
                passed_args[k] = options[k]

        # update variables dic of the instance
        self.__dict__.update(passed_args)
        # Save passed keywords arguments as a dict
        self.options = passed_args

        self.text = text
        self.set_font()
        self.margin_chr = self.margin * self.chr_w

        self.surface = pygame.Surface((self.width, self.height),  SRCALPHA)
        if self.color is not None:
            self.surface.fill(self.color)

        self.wrap_width = round(
            (self.width - 2 * self.margin_chr) / self.chr_w)
        if self.wrap_width < 0:
            print('Not enough place for the text')
            self.adjust_size = True
            self.wrap = False

    def set_font(self):
        """Set the font and its properties."""
        self.font = pygame.font.SysFont(self.fontname, self.fontsize)
        self.font.set_bold(self.bold)
        self.font.set_italic(self.italic)
        self.font.set_underline(self.underline)

        self.line_h = self.font.get_linesize()

        # calculate average width of characters
        lower = string.ascii_lowercase
        upper = string.ascii_uppercase
        digits = string.digits
        punct = string.punctuation
        random.seed(10)
        random_text = lorem.paragraph()
        text = f'{lower} {upper} {digits} {punct} {random_text}'
        text_w, text_h = self.font.size(text)

        self.chr_w = round(text_w/len(text))

    def render_line(self, text=None):
        """Render one line text into an image surface."""
        if text == None:
            text = self.text

        text_surface = self.font.render(text, True, self.fontcolor, self.color)

        return text_surface

    def render_multilines(self, text=None):
        """Render multiline texts into an image surface."""
        if self.wrap:
            wrapped = wrap(text, width=self.wrap_width,
                           replace_whitespace=False)
        else:
            wrapped = text,

        lines = list()
        for line in wrapped:
            l = line.split('\n')
            for chunk in l:
                lines.append(chunk)

        self.lines = lines

        # find largest text width among lines to define width of the text surface box
        max_width = 0
        for i, line in enumerate(self.lines):
            line_w, _ = self.font.size(line)
            max_width = line_w if line_w > max_width else max_width

        # set the width/height of text surface
        h = self.line_h
        n = len(lines)

        # text surface box
        text_surface = pygame.Surface(
            (max_width, (n-1) * self.interline * h + h), flags=SRCALPHA)
        if self.color is not None:
            text_surface.fill(self.color)

        # blit lines into text surface box
        for i, line in enumerate(self.lines):
            # print(line)
            txt = self.render_line(text=line)
            y = self.interline * h * i
            text_surface.blit(txt, (0, y))

        return text_surface

    @staticmethod
    def _defaults():
        defaults = {
            'fontname': None,
            'fontsize': 18,
            'fontcolor': 'black',

            'italic': False,
            'bold': False,
            'underline': False,

            'width': 150,
            'h_align': 1,  # 0=left, 1=center, 2=right
            'color': None,

            'height': 20,
            'v_align': 1,  # 0=top, 1=center, 2=bottom

            'margin': 1,  # number of characters margin, base on capital T character
            'interline': 1,

            'wrap': True,

            'adjust_size':  False,
        }

        return defaults.copy()


class Text(TextAssets):
    """Create a text object within a box, allowing alignmet of the text within the box.

    Notice that window has to be given, but it is not used for the construction of the text.
    The resulting rect attribute is always positioned at 0,0
    The surface box size is based on the width and height given by the user, if 'adjust_size' is true, then the size can be adjusted so that the box covers the integrity of the text.
    """

    def __init__(self, window, text='Text', **options):
        super().__init__(window, text, **options)

        self.text = None
        self.set_text(text)
        self.text = text

    def set_text(self, text):
        # this keeps the size of the original surface
        if text == self.text:
            return

        self.text = text
        self.text_surface = None
        new_line = text.find('\n')
        long_text =  len(text)>self.wrap_width and len(text)> self.min_wrap_width

        # print(new_line)
        if new_line == -1 and not long_text :
            self.text_surface = self.render_line(text)
        else:
            self.text_surface = self.render_multilines(text)

        x, y = self.include_aligned(self.text_surface
                             , margin = self.margin_chr
                             , h_align = self.h_align
                             , v_align = self.v_align
                             , adjust_size = self.adjust_size
                           )
        # draw text into asset's surface
        self.surface.blit(self.text_surface, (x, y))


class ButtonAssets(Asset):
    # Constants used to track the state of the button
    states =  ['default', 'hover' , 'pressed']

    # @abstractmethod
    def __init__(self, window,  enter_activated , **options):

        passed_args = self._defaults()

        for k in options: # overwrite defaults
            if k in passed_args:
                passed_args[k] = options[k]

        self.__dict__.update(passed_args)
        super().__init__(window)

        self._state  = 'default'
        self.enter_activated = enter_activated
        self.options = passed_args
        self.rect = (0,0, self.width, self.height)


    def handle(self, event):
        """Change button current state and return true when button is clicked."""
        if not self.enabled:
            return False
        if not self.visible:
            return False

        # hit by pressing return
        if self.enter_activated:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.state = 'default'
                    return True

        # return false for not relevant events
        if event.type not in (MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN):
            # The button only cares about mouse-related events
            return False  # early exit

        # return false for any event outside focus
        if not self.hovering(event.pos):
            # print(f'{self.state=}')
            self.state = 'default'
            return False
        # but in focus
        else: # if hovering
            if self.state == 'default':
                self.state = 'hover'
                # print(f'{self.state=}')
                return False
            elif self.state == 'hover':
                if event.type == MOUSEBUTTONDOWN:
                    self.state = 'pressed'
                    # print(f'{self.state=}')
                    return False
            elif self.state == 'pressed':
                if event.type == MOUSEBUTTONUP:
                    # hit, a new start
                    self.state ='hover'
                    # print(f'{self.state=}')
                    return True

    @staticmethod
    def _defaults():
        # so far this is only relevant for Button
        defaults = {
                    'fontname': None,
                    'fontsize': 24,
                    'fontcolor': 'black',

                    'italic': False,
                    'bold': False,
                    'underline': False,

                    'width': 60,
                    'h_align': 1,  # 0=left, 1=center, 2=right
                    'color': None,

                    'height': 10,
                    'v_align': 1,  # 0=top, 1=center, 2=bottom

                    'margin' : 1, # number of characters margin, base on capital T character
                    'interline': 1,
                    'wrap': False,

                    'colors' : dict(default=(190, 190, 190)
                                            , hover =(210, 210, 210)
                                            , pressed = (140, 140, 140)
                                            , disabled = (220, 220, 220))
                    , 'fontcolors' : dict(default= 'blue'
                                            , hover = 'red'
                                            , pressed = 'green3'
                                            , disabled = 'gray')
                    ,
                    'adjust_size' : False,

        }

        return deepcopy(defaults)


class ButtonImage(ButtonAssets):
    """Create buttons from dictionary of images paths."""

    states =  ['default', 'hover' , 'pressed', 'disabled']

    def __init__(self, window, images_path, images_files, resize = None, enter_activated=False , **options):
        # images_path
        # images_files dict with the name of the files and the state
        # resize tuple with width and hight
        super().__init__(window, enter_activated, **options)
        self.images_path  = images_path
        self.images_files  = images_files
        self.resize = resize
        self.images = dict()
        self.images_to_surface()
        self.surface = self.images['default']

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self.surface = self.images[state]
        self._state = state

    # Create the button's Surface objects.
    def images_to_surface(self):
        for state, file in self.images_files.items():

            _file = path.join(self.images_path, file)
            # print(_file)
            img = pygame.image.load(_file)
            if self.resize is not None:
                img = pygame.transform.smoothscale(img ,  self.resize)

            self.images[state] = img

class ButtonImageActivate(ButtonAssets):
    """Create image button that can turn on/off a game setting such as sound/silence.
    It allows for different images depending on its on/off status."""

    states =  ['default', 'hover' , 'pressed', 'disabled']

    def __init__(self, window, images_path, images_true_files, images_false_files, resize = None, enter_activated=False , **options):
        # images_path
        # images_files dict with the name of the files and the state
        # resize tuple with width and hight
        super().__init__(window, enter_activated, **options)
        self.images_path  = images_path
        self.images_true_files  = images_true_files
        self.images_false_files  = images_false_files
        self.resize = resize
        self.images_true = dict()
        self.images_false = dict()
        self.images_to_surface()
        self.on = True
        self.surface = self.images_true['default'] if  self.on else self.images_false['default']

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self.surface = self.images_true[state] if self.on else self.images_false[state]
        self._state = state


    # Create the button's Surface objects.
    def images_to_surface(self):

        for state, file in self.images_true_files.items():
            _file = path.join(self.images_path, file)
            # print(_file)
            img = pygame.image.load(_file)
            if self.resize is not None:
                img = pygame.transform.smoothscale(img ,  self.resize)

            self.images_true[state] = img

        for state, file in self.images_false_files.items():
            _file = path.join(self.images_path, file)
            # print(_file)
            img = pygame.image.load(_file)
            if self.resize is not None:
                img = pygame.transform.smoothscale(img ,  self.resize)

            self.images_false[state] = img



class Button(ButtonAssets):
    """Simple button created from text."""

    dark_gray = (64, 64, 64)
    gray = (128, 128, 128)
    min_width = 40
    states =  ['default', 'hover' , 'pressed', 'disabled']

    def __init__(self, window, text , enter_activated=False , **options):
        super().__init__(window, enter_activated, **options)

        self.text = text
        self.images  = self.text_images()
        self.surface = self.images['default'].surface
        self.box_design()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        self.surface = self.images[state].surface
        self._state = state

    # Create the button's Surface objects.
    def text_images(self):

        kargs = deepcopy(self.options)
        dic = dict()
        for state in self.colors.keys():
            kargs['fontcolor'] = self.fontcolors[state]
            kargs['color'] = self.colors[state]

            txt = Text(self.window, text = self.text, **kargs)
            dic[state] =  txt

        self.margin_chr =dic[state].margin_chr
        self.chr_w =dic[state].chr_w

        return dic

    def box_design(self):
        w, h =  self.rect.size
        line = pygame.draw.line
        dark_gray = self.dark_gray
        gray = self.gray

        for state, txt in self.images.items():
            surface = txt.surface
            if state != 'disabled' :
                line(surface, 'white', (1, 1), (w - 2, 1))
                line(surface, 'white', (1, 1), (1, h - 2))

            if state != 'hover' :
                line(surface, dark_gray, (1, h - 1), (w - 1, h - 1))
                line(surface, dark_gray, (w - 1, 1), (w - 1, h - 1))
                line(surface, gray, (2, h - 2), (w - 2, h - 2))
                line(surface, gray, (w - 2, 2), (w - 2, h - 2))

            if state == 'pressed' :
                line(surface, dark_gray, (1, h - 2), (1, 1))
                line(surface, dark_gray, (1, 1), (w - 2, 1))
                line(surface, gray, (2, h - 3), (2, 2))
                line(surface, gray, (2, 2), (w - 3, 2))
