# -*- coding: utf-8 -*-
"""
Created on Sun Mar  5 19:32:37 2023

@author: carol
"""

import pygame
from pygame.locals import (
    QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONDOWN,  MOUSEMOTION, MOUSEBUTTONUP)


def window_init(size=(500, 500), color='red'):
    """Initiate pygame and diplay surface. Handy for testing."""
    # Initializing Pygame
    pygame.init()
    # Creating the surface
    screen = pygame.display.set_mode(size)
    # convert
    # pygame.Surface.convert_alpha(screen)
    screen.fill(color)

    return screen


def loop(fps=None):
    """Set main loop. Handy for testing."""
    if fps is None:
        fps = 60

    clock = pygame.time.Clock()
    running = True

    while running:
        # Did the user click the window close button?
        for event in pygame.event.get():

            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
            if event.type == pygame.QUIT:
                running = False

        # Flip the display
        pygame.display.flip()
        clock.tick(fps)

    pygame.quit()


def exit_event(event):
    """Exit event for the main loop."""
    if event.type == KEYDOWN:
        # If the Esc key is pressed, then exit the main loop
        if event.key == K_ESCAPE:
            return True

    # Check for QUIT event. If QUIT, then set running to false.
    elif event.type == QUIT:
        return True

    # if none of the above is detected then we are running
    return False


def dragging_event(event, shape, mat):
    """Allow the user to drag a shape/asset with the mouse.

    The shape starts right away moving within the game board.
    The shape is only allowed to move within the game board.
    The shape's rect center coordinates are changed with the mouse position.

    Parameters:
    -----------
    event : pygame event. The event to check for MOUSEMOTION events.
    shape : asset object to be dragged.
    mat : asset object where the shape is allowed to move (game board)

    """
    # Get the current position of the mouse
    mx, my = pygame.mouse.get_pos()  # this is not an event

    # Get the boundaries of the mat
    top_mat = mat.rect.top
    bottom_mat = mat.rect.bottom
    left_mat = mat.rect.left
    right_mat = mat.rect.right

    def in_play_area():
        """Check if the mouse is inside the boundaries of the mat based on the position of the mouse.

        It returns a tuple of booleans (x,y) -  when it returns (True, True), it means that x,y of the mouse are within the boundaries of the mat, if it returns (False, True), then this means that the x coordenate of the mouse is out of the x range of the mat but y is within the boundaries.
        """
        x, y = True, True
        margin = shape.rect.height//2  # //2 for getting the whole shape into the game

        # check y range
        if my > bottom_mat - margin or my < top_mat + margin:
            y = False
        # check x range
        if mx > right_mat - margin or mx < left_mat + margin:
            x = False

        return x, y

    # when an event movement of the mouse within boundaries, move to the position of the mouse
    if event.type == pygame.MOUSEMOTION:
        if in_play_area() == (True, True):
            shape.rect.center = (mx, my)
        elif in_play_area() == (True, False):
            shape.rect.centerx = mx
        elif in_play_area() == (False, True):
            shape.rect.centery = my


def dragging_event_ip(event, shape):
    # this looks better than the previous
    if event.type == MOUSEBUTTONDOWN:
        if shape.hovering(event.pos):
            shape.moving = True

    elif event.type == MOUSEBUTTONUP:
        shape.moving = False

    elif event.type == MOUSEMOTION and shape.moving:
        shape.rect.move_ip(event.rel)


def selected(event, shape):
    """Switch true/false the selected attribute of an asset when clicked on.

    Parameters:
        shape : Asset object
    """
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            if shape.hovering(event.pos):
                shape.selected = not shape.selected


def single_choice(event, shape, choices):
    """Switch True the 'selected' attribute of the Asset object `shape' when clicked on.

    The selected attribute for all the other Asset objects different from share are set as False.

    Parameters:
        shape : Asset object
        choices : iterable of Asset objects.
    """
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            if shape.hovering(event.pos):
                for choice in choices:
                    if choice == shape:
                        shape.selected = True
                    else:
                        choice.selected = False


def click_on(event, shape):
    if event.type == MOUSEBUTTONDOWN:
        if event.button == 1:
            if shape.hovering(event.pos):
                return True


def hovering_event(event, shape):
    if event.type == MOUSEMOTION:
        if shape.hovering(event.pos):
            # print('hovering inside')
            return True
