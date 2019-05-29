"""
This module contains the Map class.
"""

import numpy as np
from enum import Enum

def is_on_border(i, j, w ,h):
    return i == 0 or i == w - 1 or j == 0 or j == h - 1

class Tile(Enum):
    """
    The different type of elements that can be in a map.
    """
    EMPTY = 0
    WALL = -1
    PLAYER_ONE_BODY = 1
    PLAYER_ONE_HEAD = 2
    PLAYER_TWO_BODY = 3
    PLAYER_TWO_HEAD = 4

    def color(self):
        """
        Converts an element of a map to a nice color.
        """
        if self == Tile.EMPTY:
            return (255, 255, 255)
        elif self == Tile.WALL:
            return (0, 0, 0)
        elif self == Tile.PLAYER_ONE_BODY:
            return (128, 0, 0)
        elif self == Tile.PLAYER_ONE_HEAD:
            return (255, 0, 0)
        elif self == Tile.PLAYER_TWO_BODY:
            return (0, 128, 0)
        elif self == Tile.PLAYER_TWO_HEAD:
            return (0, 255, 0)
        else:
            return None

class Map:
    """
    The map of the game.

    It basically consists of a matrix with a certain width and height. You can
    access its items by using the [] operator.
    """
    def __init__(self, w, h, empty, wall):
        """
        Creates a new map from its width and its height.

        The map will contain (height + 2) * (width + 2) tiles, by having a
        border. The matrix is initialized with `empty` in the inside and
        `wall` on the borders.
        """
        self.width = w
        self.height = h
        self._data = np.array([[wall if is_on_border(i, j, w + 2, h + 2) else empty for i in range(h + 2)] for j in range(w + 2)])

    def clone(self):
        """
        Creates a clone of the map.
        """
        clone = Map(self.width, self.height, 0, 0)
        clone._data = np.copy(self._data)
        return clone

    def apply(self, converter):
        """
        Converts a map by applying a function to each element.
        """
        converted = Map(self.width, self.height, 0, 0)
        converted._data = np.array([[converter(self._data[i][j]) for i in range(self.height + 2)] for j in range(self.width + 2)])
        return converted

    def array(self):
        """
        Returns the inner array of the map.
        """
        return self._data

    def clone_array(self):
        """
        Returns a copy of the inner array of the map.
        """
        #return np.array([[converter(self._data[i][j]) for i in range(self.height + 2)] for j in range(self.width + 2)])
        clone_map = self.clone()
        return clone_map._data

    def color(self, t, p):
        """
        Converts an element of a map into an element to be perceived by player p.
        """
        if t == Tile.EMPTY:
            return 1
        elif t == Tile.WALL:
            return -1
        elif t == Tile.PLAYER_ONE_BODY:
            return -1
        elif t == Tile.PLAYER_ONE_HEAD:
            return 10 if p == 1 else -10
        elif t == Tile.PLAYER_TWO_BODY:
            return -1
        elif t == Tile.PLAYER_TWO_HEAD:
            return 10 if p == 2 else -10
        else:
            return None

    def state_for_player(self, p):
        """
        Returns an image representing the current perception of the environment from player p.
        """
        return self.apply(lambda tile: self.color(tile, p)).array()

    def __getitem__(self, index):
        (i, j) = index
        return self._data[i+1][j+1]

    def __setitem__(self, position, other):
        (i, j) = position
        self._data[i+1][j+1] = other

