import pygame

from utils import config


class DisplayManager:
    """Class that manage the display."""

    def __init__(self, snake, apple):
        self.__display = pygame.display.set_mode((config.DISPLAY_WIDTH, config.DISPLAY_HEIGHT))
        self.__side = config.RECT_SIZE
        self.__snake = snake
        self.__apple = apple

    def draw_grid(self):
        """Display the grid of the arena."""
        if config.DRAW_GRID:
            for x in range(config.GRID_SIZE[0]):
                for y in range(config.GRID_SIZE[1]):
                    pygame.draw.rect(self.__display, config.GRID_BORDER_COLOR,
                                     pygame.Rect(x * self.__side[0], y * self.__side[1], self.__side[0],
                                                 self.__side[1]), 1)

    def display_snake(self):
        """Display the snake on the window."""
        pos = self.__snake.position[0]
        pygame.draw.rect(self.__display, config.SNAKE_HEAD_COLOR,
                         pygame.Rect(pos[0], pos[1], self.__side[0] - 1, self.__side[1] - 1))

        for pos in self.__snake.position[1:]:
            pygame.draw.rect(self.__display, config.SNAKE_TAIL_COLOR,
                             pygame.Rect(pos[0], pos[1], self.__side[0] - 1, self.__side[1] - 1))

    def display_apple(self):
        """Display the apple on the window."""
        pygame.draw.rect(self.__display, config.APPLE_COLOR,
                         pygame.Rect(self.__apple.position[0], self.__apple.position[1], self.__side[0],
                                     self.__side[1]))

    def draw(self, score):
        """Called by the Game Manager to draw the objects needed."""
        self.__display.fill(config.BLACK)
        self.draw_grid()
        self.display_snake()
        self.display_apple()
        pygame.display.set_caption("Genetic Snake - SCORE: " + str(score))
        pygame.display.update()
