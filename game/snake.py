import numpy

from utils import config


class Snake:
    """Class that represent the snake inside the game."""

    def __init__(self):
        self.position = numpy.array([
            [(config.GRID_SIZE[0] / 2) * config.RECT_SIZE[0], (config.GRID_SIZE[1] / 2 - 3) * config.RECT_SIZE[1]],
            [(config.GRID_SIZE[0] / 2) * config.RECT_SIZE[0], (config.GRID_SIZE[1] / 2 - 2) * config.RECT_SIZE[1]],
            [(config.GRID_SIZE[0] / 2) * config.RECT_SIZE[0], (config.GRID_SIZE[1] / 2 - 1) * config.RECT_SIZE[1]],
            [(config.GRID_SIZE[0] / 2) * config.RECT_SIZE[0], (config.GRID_SIZE[1] / 2) * config.RECT_SIZE[1]]
        ])
        self.length = 4

    def move_snake(self, action):
        """Move the snake based on the Action."""
        for i in range(self.length - 1, 0, -1):
            self.position[i] = self.position[i - 1]
        self.position[0] += action

    def add_piece(self):
        """Add config.PIECE_FOR_APPLE new pieces to the Snake."""
        for value in range(config.PIECE_FOR_APPLE):
            arr = self.position[self.length - 1]
            self.position = numpy.vstack((self.position, arr))
            self.length += 1
