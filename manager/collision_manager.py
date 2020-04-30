import numpy

from utils import config


def collision_with_apple(apple_position, snake_position):
    """Return True in case of collision with the apple."""
    return numpy.array_equal(apple_position, snake_position)


def collision_with_wall(snake_position):
    """Return True in case of collision with the walls."""
    if ((snake_position[0] >= config.DISPLAY_WIDTH) | (snake_position[0] < 0)) | (
            (snake_position[1] >= config.DISPLAY_HEIGHT) | (snake_position[1] < 0)):
        return True
    return False


def collision_with_self(snake_next_position, snake):
    """Return True in case of collision with itself."""
    snake_next_position = snake_next_position.tolist()
    if snake_next_position in snake.position[1:].tolist():
        return True
    return False
