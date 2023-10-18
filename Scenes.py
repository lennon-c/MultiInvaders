# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 11:35:11 2023

@author: carol
"""
import pygame
from abc import ABC, abstractmethod
import  sys

class Scene_mgr():
    """Scene manager. To be called in the main.py file."""

    def __init__(self, scenes, size , fps = 30):
        """Initiate pygame, display window, Scenes and set current scene.

        Parameters
        ----------
        scenes : list of scene Classes
        size (width, height) : tuple or list with the width and height in pixels of the diplay
        fps :  frames per second. The default is 30.
        """
        pygame.init()
        self.window = pygame.display.set_mode(size)

        # Build a dictionary {scene key : scene object}
        self.scenes_dic = dict()
        # list of scene objects
        self.scenes_lst = list()
        for scene in scenes:
            value = scene(self.window) # initiate instance into value
            key = value.id  # each scene must return a unique key to identify itself
            self.scenes_dic[key] = value
            self.scenes_lst.append(value)

        # The first element in the list is the starting scene
        self.current = self.scenes_lst[0]

        # set parameters for the main loop
        self.fps = fps
        self.running = True

        # Give each scene a reference back to the Scene_mgr.
        for key, scene in self.scenes_dic.items():
            scene._set_mgr(self) # this writes the current manager object as an attribute of the scene instance

    def run(self):
        """Run the main loop and the event loop."""
        clock = pygame.time.Clock()
        # Main loop
        while self.running :

            # gather keys
            keys_down = pygame.key.get_pressed()

            # event loop for exit
            events = []
            for event in pygame.event.get():
                if (event.type == pygame.QUIT) or \
                        ((event.type == pygame.KEYDOWN) and
                        (event.key == pygame.K_ESCAPE)):
                    # Save user settings before leaving
                    self.current.user.save()
                    # Tell current scene we're leaving
                    self.current.leave()
                    self.running = False

                events.append(event)

            # event loops within scenes
            self.current.handle(events, keys_down)

            # draw, update FRAMES
            self.current.update()
            self.current.draw()

            # Update the window
            pygame.display.update()

            # Slow things down a bit
            clock.tick(self.fps)

        # here it can be a good place to save parameters before leaving
        pygame.quit()
        sys.exit()


    def _go_to(self, next_scene_id, data):
        """CL : I will not use the data argument, it is better to create a mother scene with a dic containing the data that can be updated and acceced by all children scenes.

        Called by a Scene, tells the Scene_mgr to go to another scene

        (From the Scene's point of view, it just needs to call its own goToScene method)
        This method:
        - Tells the current scene that it is leaving, calls leave method
        - Gets any data the leaving scene wants to send to the new scene
        - Tells the new scene that it is entering, calls enter method

        Raises:
        - KeyError if the nextSceneKey is not valid

        """
        if next_scene_id is None:  # meaning, exit
            self.running = False

        # Call the leave method of the old scene to allow it to clean up.
        self.current.leave()

        pygame.key.set_repeat(0) # turn off repeating characters
        # Set the new scene (based on the key) and
        try:
            self.current = self.scenes_dic[next_scene_id]
        except KeyError:
            raise KeyError("Trying to go to scene '" + next_scene_id +
                "' but that key is not in the dictionary of scenes.")
        # call the enter method of the new scene.
        self.current.enter(data)



class Scene(ABC):
    """The Scene class is an abstract class to be used as a base class for any scenes of the game.

    In the __init__ method of the scene subclass, you will need:

        def __init__(self, window):
            self.window = window
            self.id = 'intro'
            ... and any initialization you want to do here.
    """

    def __del__(self):
        """Call it when the scene is about to die."""
        # print('ending scene')
        self.mgr = None  # eliminate the reference to the Scene_mgr

    def _set_mgr(self, mgr):
        """Save a reference to the Scene_mgr object.

        This reference is used by the go_to.Do not change or override this method.
        """
        self.mgr = mgr

    def enter(self, data):
        """Call it when a user enters a scene.

        Should be overridden if you expect data when your scene is entered.
        Add any code you need to start or re-start the scene

        Parameters:
            |    data - can be of any type agreed to by the old and new scenes

        """
        pass

    @abstractmethod
    def handle(self, events, keyPressedList):
        """Handle events and key presses of the scene. To be called within the event loop.

        Parameters:
            |    events - a list of events your method should handle.
            |    keyPressedList - a list of keys that are pressed (a Boolean for each key).

        """
        raise NotImplementedError

    def update(self):
        """Update frame, for evry frame within the scene. To be called in the main loop."""
        pass

    @abstractmethod
    def draw(self):
        """Draw assets in the frame. To be called in the main loop."""
        raise NotImplementedError

    def leave(self):
        """Call this method whenever the user leaves a scene."""
        pass

    def quit(self):
        """Call this method if you want to quit, from inside a scene."""
        self.go_to(None)


    def go_to(self, nextSceneKey, data=None):
        """Call this method whenever you want to go to a new scene.

        Parameters:
            |    nextSceneKey - the scene key (string) of the scene to go to
            |    data - any data you want sent to the next scene (defaults to None)
            |          (The data can be a single value, a list, dictionary, object, etc.)

        """
        self.mgr._go_to(nextSceneKey, data)