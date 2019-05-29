"""
This module contains the classes that helps us watch a game of tron.
"""

import pygame

class Window:
    """
    This class represents a window, with the functions to help us render a game.
    """
    def __init__(self, game, factor):
        """
        Creates a new window from a game

        Factor is the size of a square of the tron.
        """
        self.factor = factor

        (width, height) = (factor * (game.width + 2), factor * (game.height + 2))

        self.screen = pygame.display.set_mode((width, height))
        self.render_map(game.map())

    def scale_box(self, row, col, width, height):
        """
        Rescale a box depending on the factor of the window.
        """
        return [row * self.factor, col * self.factor, width * self.factor, height * self.factor]

    def render_map(self, game_map):
        """
        Renders a map on the screen.
        """
        self.screen.fill((0, 0, 0))

        pygame.draw.rect(
            self.screen,
            (255, 255, 255),
            self.scale_box(1, 1, game_map.width, game_map.height))

        for row in range(game_map.height):
            for col in range(game_map.width):
                block = game_map[row,col]
                if block:
                    pygame.draw.rect(
                        self.screen,
                        block.color(),
                        self.scale_box(col+1.1, row+1.1, 0.9, 0.9))

        pygame.display.flip()
