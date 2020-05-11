import random

import numpy
import pygame

import manager.collision_manager as collision_manager
import utils.action as Action
from game.apple import Apple
from game.snake import Snake
from genetic_algorithm.neural_network import NeuralNetwork
from manager.display_manager import DisplayManager
from utils import config


class GameManager:
    def __init__(self, weights, apple_position=None):
        self.__snake = Snake()
        self.__apple = Apple(numpy.array([0, 0]))
        self.__score = 0
        self.__clock = pygame.time.Clock()
        self.__weights = weights
        self.__remaining_moves = config.MOVES
        self.__display_manager = DisplayManager(self.__snake, self.__apple)
        self.__time_alive = 0
        self.__apple_position = apple_position
        self.__neural_network = NeuralNetwork(self.__weights)

    def directions_distance_objects(self):
        front_direction_vector = self.__snake.position[0] - self.__snake.position[1]
        left_direction_vector = numpy.array([front_direction_vector[1], -front_direction_vector[0]])
        right_direction_vector = numpy.array([-front_direction_vector[1], front_direction_vector[0]])

        vision = numpy.zeros((0, 1))
        for vector in [left_direction_vector, front_direction_vector, right_direction_vector]:
            objects = self.get_objects_by_direction(vector)
            vision = numpy.append(vision, objects[0])
            vision = numpy.append(vision, objects[1])
            vision = numpy.append(vision, objects[2])
        return vision

    def get_objects_by_direction(self, direction):
        end = False
        found_apple = False
        found_self = False
        distance = 0
        objects = numpy.zeros((3, 1))
        while not end:
            distance += 1
            snake_position = self.__snake.position[0] + direction * distance
            if collision_manager.collision_with_wall(snake_position):
                objects[0] = 1 / distance
                end = True
            if not found_apple and collision_manager.collision_with_apple(self.__apple.position, snake_position):
                objects[1] = 1 / distance
                found_apple = True
            if not found_self and collision_manager.collision_with_self(snake_position, self.__snake):
                objects[2] = 1 / distance
                found_self = True
        return objects

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

    def check_if_game_ended(self):
        result = False
        next_position = self.__snake.position[0] + numpy.array([0, 0])
        if self.__remaining_moves <= 0:
            result = True

        if collision_manager.collision_with_wall(self.__snake.position[0]):
            result = True

        if collision_manager.collision_with_self(next_position, self.__snake):
            result = True

        return result

    def spawn_apple(self):
        apple_position = numpy.array([random.randint(1, config.GRID_SIZE[0] - 1) * config.RECT_SIZE[0],
                                      random.randint(1, config.GRID_SIZE[1] - 1) * config.RECT_SIZE[1]])
        while collision_manager.collision_with_self(apple_position, self.__snake):
            apple_position = numpy.array([random.randint(1, config.GRID_SIZE[0] - 1) * config.RECT_SIZE[0],
                                          random.randint(1, config.GRID_SIZE[1] - 1) * config.RECT_SIZE[1]])

        return apple_position

    def get_action_from_nn(self):
        vision = self.directions_distance_objects()
        vision = numpy.append(vision, self.angle_with_apple())
        self.__neural_network.update_parameters(vision)
        nn_output = self.__neural_network.get_action()

        new_direction = numpy.array(self.__snake.position[0]) - numpy.array(self.__snake.position[1])
        if nn_output == 0:
            new_direction = numpy.array([new_direction[1], -new_direction[0]])
        if nn_output == 2:
            new_direction = numpy.array([-new_direction[1], new_direction[0]])

        if new_direction.tolist() == [config.RECT_SIZE[0], 0]:
            action = Action.RIGHT
        elif new_direction.tolist() == [-config.RECT_SIZE[0], 0]:
            action = Action.LEFT
        elif new_direction.tolist() == [0, config.RECT_SIZE[1]]:
            action = Action.DOWN
        else:
            action = Action.UP
        return action

    def calculate_fitness(self):
        fitness = self.__time_alive + ((2 ** self.__snake.length) + (self.__snake.length ** 2.1) * 500) - (
                ((.25 * self.__time_alive) ** 1.3) * (self.__snake.length ** 1.2))
        fitness = max(fitness, .1)
        return fitness

    def collision_with_apple(self):
        self.__score += 1
        self.__remaining_moves += config.APPLE_EXTRA_MOVES
        self.__snake.add_piece()
        if self.__remaining_moves > config.MAX_MOVES:
            self.__remaining_moves = config.MAX_MOVES
        if self.__apple_position is not None:
            self.__apple.position = self.__apple_position[self.__score]
        else:
            self.__apple.position = self.spawn_apple()
        return self.__apple.position

    def play_game(self):
        apple_position = []
        if self.__apple_position is not None:
            self.__apple.position = self.__apple_position[self.__score]
        else:
            self.__apple.position = self.spawn_apple()
        apple_position.append(self.__apple.position)
        ended_game = False
        while ended_game is not True:
            self.__display_manager.draw(self.__score)
            self.__snake.move_snake(self.get_action_from_nn())
            self.__remaining_moves -= 1
            self.__time_alive += 1

            if collision_manager.collision_with_apple(self.__apple.position, self.__snake.position[0]):
                apple_position.append(self.collision_with_apple())

            ended_game = self.check_if_game_ended()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    ended_game = True

            self.__clock.tick(config.FPS)
        return self.calculate_fitness(), apple_position
