from utils import config


class Apple:
    """Class that represent the Apple inside of game."""

    def __init__(self, position):
        self.position = position
        self.points = config.APPLE_POINTS
