"""
This module contains everything related to the players and the controls.
"""

from enum import Enum


class Direction(Enum):
    """
    This enum represents the different directions a tron can go to.
    """
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4


class Player(object):
    """
    This is the base class for decisions.

    If you want to create a new algorithm for decisions, you should create a
    class that derives this one.
    """
    def __init__(self):
        pass

    def find_file(self, name):
        """
        Returns the correct path for finding an asset file (like neural network
        weights file) in the directory where the Ai class is.

        :name the name of the file to look for
        """
        return '/'.join(self.__module__.split('.')[:-1]) + '/' + name

    def next_position(self, current_position, direction):
        """
        Computes the next position if the player would go on towards a specific
        direction.
        """
        if direction == Direction.UP:
            return (current_position[0] - 1, current_position[1])
        if direction == Direction.RIGHT:
            return (current_position[0], current_position[1] + 1)
        if direction == Direction.DOWN:
            return (current_position[0] + 1, current_position[1])
        if direction == Direction.LEFT:
            return (current_position[0], current_position[1] - 1)

    def next_position_and_direction(self, current_position, id, map):
        """
        Computes the direction of the player, and computes its next position
        depending on the current position.
        """
        direction = self.action(map, id)
        return (self.next_position(current_position, direction), direction)

    def action(self, map, id):
        """
        This function is called each time to ask the player his action.

        It needs to return a direction, and can analyse the game map to make
        its decision.
        """
        pass

    def manage_event(self, event):
        """
        This function is called when an event occurs on the window.

        It is necessary to play the game with the keyboard.
        """
        pass


class Mode(Enum):
    """
    The different type of interaction for the keyboard controls.

    This will allow to play with two humans.
    """
    ARROWS = 1
    ZQSD = 2


class KeyboardPlayer(Player):
    """"
    This is the key board interaction.

    It uses keys depending on the mode.
    """
    def __init__(self, initial_direction, mode = Mode.ARROWS):
        """
        Creates a keyboard decision with a default direction.
        """
        super(KeyboardPlayer, self).__init__()
        self.direction = initial_direction
        self.mode = mode

    def left(self):
        """
        Returns the left key of the player depending on the mode.
        """
        import pygame
        return pygame.K_q if self.mode == Mode.ZQSD else pygame.K_LEFT

    def right(self):
        """
        Returns the right key of the player depending on the mode.
        """
        import pygame
        return pygame.K_d if self.mode == Mode.ZQSD else pygame.K_RIGHT

    def down(self):
        """
        Returns the down key of the player depending on the mode.
        """
        import pygame
        return pygame.K_s if self.mode == Mode.ZQSD else pygame.K_DOWN

    def up(self):
        """
        Returns the up key of the player depending on the mode.
        """
        import pygame
        return pygame.K_z if self.mode == Mode.ZQSD else pygame.K_UP

    def manage_event(self, event):
        """
        Changes the direction of the tron depending on the keyboard inputs.
        """
        import pygame
        if event.type == pygame.KEYDOWN:
            if event.key == self.left():
                self.direction = Direction.LEFT
            if event.key == self.up():
                self.direction = Direction.UP
            if event.key == self.right():
                self.direction = Direction.RIGHT
            if event.key == self.down():
                self.direction = Direction.DOWN

    def action(self, map, id):
        """
        Returns the direction of the tron.
        """
        return self.direction


class ConstantPlayer(Player):
    """
    This is a class that always returns the same decision.
    """
    def __init__(self, direction):
        super(ConstantPlayer, self).__init__()
        self.direction = direction

    def action(self, map, id):
        return self.direction
