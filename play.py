#!/usr/bin/env python

# Import pygame without printing anything on the terminal
import pygame

from tron.map import Map
from tron.game import Game, PositionPlayer
from tron.window import Window
from tron.player import Direction, KeyboardPlayer, Mode

# This script shows how to create a game with human players and play it interactively.
# It shows how to create the game, to setup interactive controls for users, and
# to run the game while rendering it on a window with a reasonnable framerate.

def main():
    # Initialize the game engine
    pygame.init()

    # Prepare the size for the game.
    # Those values may be good if you want to play, they might not be so good
    # to train your AI. Decreasing them will make the learning faster.
    width = 10
    height = 10

    # Create a game from its size and its players
    game = Game(width, height, [
        # We create two PositionPlayer for each player of the game.
        # The first one has the id 1, and will use keyboard interaction, with a
        # default direction that will be to the right, and that will use the Z,
        # Q, S and D keys.
        # The last array defines the initial position of the player.
        PositionPlayer(1, KeyboardPlayer(Direction.RIGHT, Mode.ZQSD), [0, 0]),

        # We create a second player that will use the arrow keys.
        PositionPlayer(2, KeyboardPlayer(Direction.LEFT, Mode.ARROWS), [width - 1, height - 1]),
    ])

    # Create a window for the game so the players can see what they're doing.
    window = Window(game, 10)

    # Hide mouse
    pygame.mouse.set_visible(False)

    # Run the game.
    game.main_loop(window)

    # Once the game is finished, if game.winner is None, it means it's a draw
    # Otherwise, game.winner will tell us which player has won the game.
    if game.winner is None:
        print("It's a draw!")
    else:
        print('Player {} wins!'.format(game.winner))

if __name__ == '__main__':
    main()

