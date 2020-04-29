from utils import config


class Apple:
    """Class that represent the Apple inside of game."""

    def __init__(self, position):
        self.__position = position
        self.__points = config.APPLE_POINTS

    def position(self, position=None):
        """If position is none then return Apple position, otherwise assign a new value to Apple position."""
        if position is None:
            return self.__position
        self.__position = position
        return self

    def points(self, points=None):
        """If points is none then return Apple points, otherwise assign a new value to Apple points."""
        if points is None:
            return self.__points
        self.__points = points
        return self
