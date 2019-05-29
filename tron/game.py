"""
This module contains everything related to the game.
"""

from time import sleep
from enum import Enum

from tron.map import Map, Tile

class Winner(Enum):
    PLAYER_ONE = 1
    PLAYER_TWO = 2

class PositionPlayer:
    """
    A container to store a player with is id, position and boolean indicating
    whether it's still alive or not.
    """
    def __init__(self, id, player, position):
        self.id = id
        self.player = player
        self.position = position
        self.alive = True

    def body(self):
        """
        Returns the body type of the PP depending on its id.
        """
        if self.id == 1:
            return Tile.PLAYER_ONE_BODY
        elif self.id == 2:
            return Tile.PLAYER_TWO_BODY

    def head(self):
        """
        Returns the head type of the PP depending of its id.
        """
        if self.id == 1:
            return Tile.PLAYER_ONE_HEAD
        elif self.id == 2:
            return Tile.PLAYER_TWO_HEAD


class HistoryElement:
    """
    An element from an history.

    It contains the map, but also the direction of each player during the frame.
    The directions of the players will be None at the first frame.
    """
    def __init__(self, mmap, player_one_direction, player_two_direction):
        self.map = mmap
        self.player_one_direction = player_one_direction
        self.player_two_direction = player_two_direction


class Game:
    """
    This class contains the map of the game, and the players.

    It allows to update the player depending on their strategies, and run the game.
    """

    def __init__(self, width, height, pps):
        """
        Returns a new game from its width, height, and number of players.

        Width and height are the number of blocs available in the tron map.
        """
        self.width = width
        self.height = height
        mmap = Map(width, height, Tile.EMPTY, Tile.WALL)
        self.history = [HistoryElement(mmap, None, None)]
        self.pps = pps
        self.winner = None

        for pp in self.pps:
            self.history[-1].map[pp.position[0], pp.position[1]] = pp.head()

    def map(self):
        """
        Returns a clone of the current map, the last map in the history.
        """
        return self.history[-1].map.clone()

    def next_frame(self, window = None):
        """
        Computes the next frame of the game.

        If a window is passed as parameter, events are polled and passed to the
        players, so you can play the game.
        Then, all the players are updated and if a player lands on a square
        that is already occupied or that is outside of the map, the players
        dies.

        If there is an error during the evaluation of a player strategy, the
        player will automatically lose and this function will return False.
        """

        map_clone = self.map()

        # Set previous heads to body
        for pp in self.pps:
            map_clone[pp.position[0], pp.position[1]] = pp.body()

        # Play next move
        for id, pp in enumerate(self.pps):
            try:
                (pp.position, pp.player.direction) = pp.player.next_position_and_direction(pp.position, id + 1, self.map())
            except:
                # An error occured during the evaluation of pp.player strategy
                if id == 0:
                    self.winner = 2
                elif id == 1:
                    self.winner = 1
                return False


        # Update history with newly played move
        self.history[-1].player_one_direction = self.pps[0].player.direction
        self.history[-1].player_two_direction = self.pps[1].player.direction

        # Manage the events
        if window:
            import pygame
            while True:
                event = pygame.event.poll()

                if event.type == pygame.NOEVENT:
                    break

                for pp in self.pps:
                    try:
                        pp.player.manage_event(event)
                    except:
                        # An error occured during the evaluation of pp.player strategy
                        if id == 0:
                            self.winner = 2
                        elif id == 1:
                            self.winner = 1
                        return False

        for (id, pp) in enumerate(self.pps):

            # Check boundaries
            if pp.position[0] < 0 or pp.position[1] < 0 or \
               pp.position[0] >= self.width or pp.position[1] >= self.height:

                pp.alive = False
                map_clone[pp.position[0], pp.position[1]] = pp.head()

            # Check collision
            elif map_clone[pp.position[0], pp.position[1]] is not Tile.EMPTY:
                pp.alive = False
                map_clone[pp.position[0], pp.position[1]] = pp.head()

            else:
                map_clone[pp.position[0], pp.position[1]] = pp.head()

        # Append to history
        self.history.append(HistoryElement(map_clone, None, None))

        return True

    def main_loop(self, window = None):
        """
        Loops until the game is finished

        If a window is passed as parameter, the game is rendered on the window.
        """

        if window:
            window.render_map(self.map())

        while True:
            alive_count = 0
            alive = None

            if window:
                sleep(0.1)

            if not self.next_frame(window):
                break

            for pp in self.pps:
                if pp.alive:
                    alive_count += 1
                    alive = pp.id

            if alive_count <= 1:
                if alive_count == 1:
                   # If player one and two share the same position, it will
                   # mean that they reached the same tile at the same
                   # moment, so it's really a draw.
                    if self.pps[0].position[0] != self.pps[1].position[0] or \
                       self.pps[0].position[1] != self.pps[1].position[1]:

                       # Otherwise, the winner is the player that is still alive.
                       self.winner = alive
                break

            if window:
                window.render_map(self.map())

