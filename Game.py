# -*- coding: utf-8 -*-

# from pygame.locals import MOUSEBUTTONDOWN, MOUSEMOTION
import pygame
import random

from Constants import c
from Questions import Multiplications_inv, Multiplications
from Assets import Circle, Square, Asset
import os


border_radius= 15

class Game_mgr():
    """Manage the multiplication game."""

    def __init__(self, window, mat, first_numbers, speed, game=1):
        """Create questions and answers. Define sounds for wrong and correct answers.

        Parameters
        ----------
        window : Surface. Display surface of pygame.
        mat : Asset object. The board of the game
        first_numbers : iterable of integers, including the numbers allowed as the first number of a multiplication problem.
        speed : str. Possible values: 'normal',  'fast', 'even faster'
        game : int, optional, default = 1. Type of questions. Possible values 1 and 2. If 1, the user receives a multiplication problem (i.e. 2 x 3) and has to find the correct answer to the problem, otherwise the user is given a number and has to select the multiplication problem that equals the given number.

        """
        self.window = window  # this is not necessary
        self.mat = mat  # board
        self.first_numbers = first_numbers
        self.game = game

        # questions games
        self.game_2 = Multiplications_inv(n_alternatives=c('n_alternatives'),
                                          first_numbers=self.first_numbers,
                                          second_numbers=c('second_numbers')
                                          )

        self.game_1 = Multiplications(n_alternatives=c('n_alternatives'),
                                      first_numbers=self.first_numbers,
                                      second_numbers=c('second_numbers')
                                      )

        if game == 1:
            self.multi = self.game_1
        else:
            self.multi = self.game_2

        # sounds
        correct_sound = os.path.join(c('sounds_path'), c('correct_sound'))
        wrong_sound = os.path.join(c('sounds_path'), c('wrong_sound'))
        self.correct_sound = pygame.mixer.Sound(correct_sound)
        self.wrong_sound = pygame.mixer.Sound(wrong_sound)

        # speed
        speeds = {'fast': 2  # 4
                  , 'normal': 1  # 3
                  , 'even faster': 3  # 5
                  }

        self.speed = speeds[speed]
        self.score = 0
        self.sound = True

    def circle(self, text):
        obj = Circle(self.window, text, size=c('circle_size'),
                     color=random.choice(c('colors')))

        return obj

    def rect(self, text):
        obj = Square(self.window, text, size=c('rect_size'), color=random.choice(
            c('colors')), border_radius=border_radius)

        return obj

    def create_player(self, text):
        """Create player object with question (text)."""
        if self.game == 2:
            player = self.circle(text)
        else:
            player = self.rect(text)

        return player

    def create_alternative(self, text):
        """Create an alternative object with answer (text)."""
        if self.game == 2:
            alternative = self.rect(text)
        else:
            alternative = self.circle(text)

        return alternative

    def start(self):
        """Start a new question, with its correct and alternative answers, the player and set the initial position of alternatives."""
        # pick a question
        self.multi.start()

        # create/replace player object with question number
        self.player = self.create_player(self.multi.question)

        # create alternative objects
        self.answers = list()
        for text in self.multi.alternatives:
            answer = self.create_alternative(text)
            self.answers.append(answer)

        # locate alternatives at the start
        # calculate space between alternatives (margin)
        mat_width = self.mat.rect.size[0]
        w, h = answer.rect.size
        space_free = mat_width - c('n_alternatives')*w
        margin = space_free/(c('n_alternatives') + 1)

        # x position
        Asset.grid(1, len(self.answers), self.mat, self.answers,
                   margin=margin, outer_margin=margin, adjust_size_grid=False)

        if self.variant == 'variant_1':
            # alternatives fall all at once
            height = self.answers[0].rect.height
            for answer in self.answers:
                answer.rect.y = self.mat.rect.y - \
                    height   #  
                answer.rect.x = answer.rect.x + self.mat.rect.x
                answer.window = self.window

        else:
            # alternatives fall one by one
            y = self.mat.rect.y - (h*c('n_alternatives'))
            random.shuffle(self.answers)
            for answer in self.answers:
                answer.rect.y = y
                answer.rect.x = answer.rect.x + self.mat.rect.x
                answer.window = self.window
                y = y + h

        self.over = False

    def update(self):
        """Update the game.

        Check collisions, missed, play sound, update scores. Start a new round of questions if requiered.
        """
        # Check if player has collided with any of alternatives
        # => calculate score and set game over
        for answer in self.answers:
            if self.game == 2:
                collide = self.player.collide(answer) and self.over == False
            else:
                collide = answer.collide(self.player) and self.over == False

            if collide:
                # set over true, so that only one collition/answer is evaluated
                self.over = True
                self.last_answer = f'{self.multi.question} = {self.multi.correct}'
                print(self.last_answer)
                if answer.text == self.multi.correct:
                    self.score = self.score + c('score_correct')
                    if self.sound:
                        self.correct_sound.play()
                else:
                    self.score = self.score + c('score_incorrect')
                    if self.sound:
                        self.wrong_sound.play()

        # If a collision occured,
        # => then start a new question, no check for the missings is needed
        # => return
        if self.over == True:
            # get current pos of player
            center = self.player.rect.center
            self.start()  # this sets again over as False
            # paste pos to new obj player
            self.player.rect.center = center
            return

        # If self.over = False, implies that in this round no collition has happend,
        # => then check for missed alternatives
        # over must be redundant (as all possible instance of True has been returned)
        for answer in self.answers:
            # if missed
            if answer.rect.top >= (self.mat.rect.bottom - answer.rect.height) and self.over == False:
                x = answer.rect.x
                text = answer.text
                # using just remove methode from list class
                self.answers.remove(answer)

                if text == self.multi.correct:
                    # create a correct
                    self.multi.correct = next(self.multi.cycle_corrects)
                    self.score = self.score + c('score_incorrect')
                    new_text = self.multi.correct  # n it a tuple of two numbers
                else:
                    new_text = next(self.multi.cycle_wrongs)

                # create the new alternative based on new_text
                answer = self.create_alternative(new_text)
                answer.rect.x = x  # from the place just liberated by the missed
                answer.rect.y = 0 - answer.rect.height
                self.answers.append(answer)
            else:  # answer still within board
                # update vertical position
                y = answer.rect.y
                answer.rect.y = y + self.speed

    def draw(self):
        """Draw all answers of the current question."""
        for answer in self.answers:
            answer.draw()
        self.player.draw()


if (__name__ == '__main__'):
    print('debbuging')
    """
    pygame.quit()
    """


