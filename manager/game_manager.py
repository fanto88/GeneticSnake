import random

import numpy
import pygame

import manager.collision_manager as collision_manager
# TODO: Fare che si possa anche giocare a mano e non solamente con IA?
# TODO: Check Vittoria
# TODO: Snake guarda in tutte le direzioni in torno a sè: Davanti, davanti a sinistra, sinistra, dietro sinistra,
#       davanti destra, destra, dietro destra, dietro. Per ogni direzione ha la distanza da sè, dal muro e dal cibo. 24 input.
# TODO: Input fra -1 e 1
# TODO: La mela non può spawnare dentro snake
import utils.action as Action
from game.apple import Apple
from game.snake import Snake
from genetic_algorithm.neural_network import NeuralNetwork
from manager.display_manager import DisplayManager
from utils import config


class GameManager:
    def __init__(self, weights):
        self.__snake = Snake()
        self.__apple = Apple(numpy.array([0, 0]))
        self.__score = self.__snake.length
        self.__clock = pygame.time.Clock()
        self.__weights = weights
        self.__remaining_moves = config.MOVES
        self.__display_manager = DisplayManager(self.__snake, self.__apple)
        self.__time_alive = 0

    def current_direction(self):
        return numpy.array(self.__snake.position[0]) - numpy.array(self.__snake.position[1])

    def blocked_directions(self):
        current_direction_vector = self.current_direction()
        left_direction_vector = numpy.array([current_direction_vector[1], -current_direction_vector[0]])
        right_direction_vector = numpy.array([-current_direction_vector[1], current_direction_vector[0]])

        is_front_blocked = self.is_direction_blocked(current_direction_vector)
        is_left_blocked = self.is_direction_blocked(left_direction_vector)
        is_right_blocked = self.is_direction_blocked(right_direction_vector)

        return is_front_blocked, is_left_blocked, is_right_blocked

    def get_objects_by_direction(self, direction):
        end = False
        found_apple = False
        found_self = False
        i = 0
        objects = numpy.zeros((3, 1))
        while not end:
            i += 1
            snake_position = self.__snake.position[0] + direction * i
            if collision_manager.collision_with_wall(snake_position):
                # distance = numpy.linalg.norm(numpy.array(snake_position) - numpy.array(self.__snake.position[0]))
                objects[0] = 1 / i
                end = True
            if not found_apple and collision_manager.collision_with_apple(self.__apple.position, snake_position):
                # distance = numpy.linalg.norm(numpy.array(snake_position) - numpy.array(self.__snake.position[0]))
                objects[1] = 1 / i
                found_apple = True
            if not found_self and collision_manager.collision_with_self(snake_position, self.__snake):
                # distance = numpy.linalg.norm(numpy.array(snake_position) - numpy.array(self.__snake.position[0]))
                objects[2] = 1 / i
                found_self = True
        return objects

    def directions_distance_objects(self):
        front_direction_vector = self.__snake.position[0] - self.__snake.position[1]
        left_direction_vector = numpy.array([front_direction_vector[1], -front_direction_vector[0]])
        right_direction_vector = numpy.array([-front_direction_vector[1], front_direction_vector[0]])
        """back_direction_vector = numpy.array([-front_direction_vector[0], -front_direction_vector[1]])
        front_left_direction_vector = front_direction_vector - right_direction_vector
        front_right_direction_vector = front_direction_vector - left_direction_vector
        back_left_direction_vector = back_direction_vector - right_direction_vector
        back_right_direction_vector = back_direction_vector - left_direction_vector"""

        #direction = numpy.array([-config.RECT_SIZE[0], 0])
        #direction2 = numpy.array([0, -config.RECT_SIZE[0]])
        #direction3 = numpy.array([config.RECT_SIZE[0], 0])

        vision = numpy.zeros((0, 1))
        """for vector in [front_direction_vector, left_direction_vector, right_direction_vector,
                       front_left_direction_vector, front_right_direction_vector, back_direction_vector,
                       back_right_direction_vector, back_left_direction_vector]:
            objects = self.get_objects_by_direction(vector)
            vision = numpy.append(vision, objects[0])
            vision = numpy.append(vision, objects[1])
            vision = numpy.append(vision, objects[2])"""
        objects = self.get_objects_by_direction(left_direction_vector)
        vision = numpy.append(vision, objects[0])
        vision = numpy.append(vision, objects[1])
        vision = numpy.append(vision, objects[2])
        objects = self.get_objects_by_direction(front_direction_vector)
        vision = numpy.append(vision, objects[0])
        vision = numpy.append(vision, objects[1])
        vision = numpy.append(vision, objects[2])
        objects = self.get_objects_by_direction(right_direction_vector)
        vision = numpy.append(vision, objects[0])
        vision = numpy.append(vision, objects[1])
        vision = numpy.append(vision, objects[2])
        """max = numpy.linalg.norm(numpy.array([[config.DISPLAY_WIDTH / 2, config.DISPLAY_HEIGHT / 2]]))
        min = numpy.linalg.norm(numpy.array([[config.RECT_SIZE[0], config.RECT_SIZE[1]]]))
        all_direction_distance_from_wall = numpy.interp(all_direction_distance_from_wall, (min, max), (-1, +1))
        all_direction_distance_from_apple = numpy.interp(all_direction_distance_from_apple, (min, max), (-1, +1))
        all_direction_distance_from_self = numpy.interp(all_direction_distance_from_self, (min, max), (-1, +1))
        all_direction_distance_from_wall *= -1
        all_direction_distance_from_apple *= -1
        all_direction_distance_from_self *= -1"""
        return vision

    def angle_with_apple(self):
        apple_direction_vector = numpy.array(self.__apple.position) - numpy.array(self.__snake.position[0])
        snake_direction_vector = numpy.array(self.__snake.position[0]) - numpy.array(self.__snake.position[1])

        norm_of_apple_direction_vector = numpy.linalg.norm(apple_direction_vector)
        norm_of_snake_direction_vector = numpy.linalg.norm(snake_direction_vector)
        if norm_of_apple_direction_vector == 0:
            norm_of_apple_direction_vector = 10
        if norm_of_snake_direction_vector == 0:
            norm_of_snake_direction_vector = 10

        apple_direction_vector_normalized = apple_direction_vector / norm_of_apple_direction_vector
        snake_direction_vector_normalized = snake_direction_vector / norm_of_snake_direction_vector
        angle = numpy.math.atan2(
            apple_direction_vector_normalized[1] * snake_direction_vector_normalized[0] -
            apple_direction_vector_normalized[
                0] * snake_direction_vector_normalized[1],
            apple_direction_vector_normalized[1] * snake_direction_vector_normalized[1] +
            apple_direction_vector_normalized[
                0] * snake_direction_vector_normalized[0]) / numpy.math.pi
        return angle

    def is_direction_blocked(self, direction):
        snake_next_position = self.__snake.position[0] + direction
        if (collision_manager.collision_with_wall(snake_next_position)) or (
                collision_manager.collision_with_self(snake_next_position, self.__snake)):
            return True
        return False

    def check_if_game_ended(self):
        result = False
        next_position = self.__snake.position[0] + numpy.array([0, 0])
        if self.__remaining_moves <= 0:
            result = True

        if collision_manager.collision_with_wall(self.__snake.position[0]):
            result = True
            self.__score += config.POINTS_FOR_COLLISION

        if collision_manager.collision_with_self(next_position, self.__snake):
            result = True
            self.__score += config.POINTS_FOR_COLLISION

        return result

    def spawn_apple(self):
        apple_position = numpy.array([random.randint(1, config.GRID_SIZE[0] - 1) * config.RECT_SIZE[0],
                                      random.randint(1, config.GRID_SIZE[1] - 1) * config.RECT_SIZE[1]])
        while collision_manager.collision_with_self(apple_position, self.__snake):
            apple_position = numpy.array([random.randint(1, config.GRID_SIZE[0] - 1) * config.RECT_SIZE[0],
                                          random.randint(1, config.GRID_SIZE[1] - 1) * config.RECT_SIZE[1]])

        return apple_position

    def play_game(self):
        self.__apple.position = self.spawn_apple()
        ended_game = False
        neural_network = NeuralNetwork(self.__weights)
        while ended_game is not True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ended_game = True

            self.__display_manager.draw()
            vision = self.directions_distance_objects()
            vision = numpy.append(vision, self.angle_with_apple())
            neural_network.update_parameters(vision)

            index = neural_network.get_action()
            new_direction = numpy.array(self.__snake.position[0]) - numpy.array(self.__snake.position[1])
            if index == 0:
                new_direction = numpy.array([new_direction[1], -new_direction[0]])
            if index == 2:
                new_direction = numpy.array([-new_direction[1], new_direction[0]])
            if new_direction.tolist() == [config.RECT_SIZE[0], 0]:
                action = Action.RIGHT
            elif new_direction.tolist() == [-config.RECT_SIZE[0], 0]:
                action = Action.LEFT
            elif new_direction.tolist() == [0, config.RECT_SIZE[1]]:
                action = Action.DOWN
            else:
                action = Action.UP

            """vision = self.directions_distance_objects()
            vision = numpy.atleast_2d(vision)

            output = keras.neural_net(self.__weights).model.predict(vision, 1)[0]
            output = numpy.argmax(output)
            new_direction = numpy.array(self.__snake.position[0]) - numpy.array(self.__snake.position[1])
            if output == 0:
                new_direction = numpy.array([new_direction[1], -new_direction[0]])
            if output == 2:
                new_direction = numpy.array([-new_direction[1], new_direction[0]])
            if new_direction.tolist() == [config.RECT_SIZE[0], 0]:
                action = Action.RIGHT
            elif new_direction.tolist() == [-config.RECT_SIZE[0], 0]:
                action = Action.LEFT
            elif new_direction.tolist() == [0, config.RECT_SIZE[1]]:
                action = Action.DOWN
            else:
                action = Action.UP"""
            self.__snake.move_snake(action)
            self.__remaining_moves -= 1
            self.__time_alive += 1

            if collision_manager.collision_with_apple(self.__apple.position, self.__snake.position[0]):
                self.__score += self.__apple.points
                self.__remaining_moves += config.APPLE_EXTRA_MOVES
                self.__apple.position = self.spawn_apple()
                self.__snake.add_piece()
            pygame.display.set_caption("Genetic Snake - SCORE: " + str(self.__score))
            ended_game = self.check_if_game_ended()
            self.__clock.tick(config.FPS)

        fitness = (self.__time_alive) + ((2**self.__snake.length) + (self.__snake.length**2.1)*500) - (((.25 * self.__time_alive)**1.3) * (self.__snake.length**1.2))
        fitness = max(fitness, .1)

        return fitness
