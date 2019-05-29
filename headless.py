#!/usr/bin/env python3

from tron.map import Map
from tron.game import Game, PositionPlayer
from tron.player import Direction, ConstantPlayer

# This script shows how to create a game with AI, that will run automatically.
# It is made to be fast and not to be used by humans. It especially doesn't
# display any window and doesn't listen to any keystrokes.

def main():
    # Prepare the size for the game.
    # Those values may be good if you want to play, they might not be so good
    # to train your AI. Decreasing them will make the learning faster.
    width = 10
    height = 10

    # Create a game from its size and its players
    game = Game(width, height, [
        # Here we create two players with constant direction.
        # It's not very interesting but it's the basis of everything else.
        PositionPlayer(1, ConstantPlayer(Direction.RIGHT), [0, 0]),
        PositionPlayer(2, ConstantPlayer(Direction.LEFT), [width - 1, height - 1]),
    ])

    # Run the game.
    # Since no window is passed as parameter, not only the game will not
    # display anything, which avoid doing useless computations, but it will
    # also not be limited to a certain framerate, which would be necessary for
    # human users.
    game.main_loop()

    # The game is done, you can get information about it and do what you want.
    if game.winner is None:
        print("It's a draw!")
    else:
        print('Player {} wins!'.format(game.winner))

if __name__ == '__main__':
    main()

