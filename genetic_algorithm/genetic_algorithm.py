import random

import numpy

from manager.game_manager import GameManager
from utils import config


def calculate_fitness(population):
    """Calculate the fitness value for the entire population of the generation."""
    # First we create all_fit, an empty array, at the start. Then we proceed to start the chromosome x and we will
    # calculate his fit_value. Then we will insert, inside the all_fit array, all the fit_values for each chromosome
    # of the population and return the array. max_points is used to return all the apple positions of the game with
    # the best snake so that we can watch again the game later
    all_fit = []
    apple_position = []
    max_points = 0
    for i in range(len(population)):
        fit_value = 0
        points, apples = GameManager(population[i]).play_game()
        if points > max_points:
            apple_position = apples.copy()
            max_points = points
        fit_value += points
        all_fit.append(fit_value)
    return all_fit, apple_position


def select_best_individuals(population, fitness):
    """Select X number of best parents based on their fitness score."""
    # Create an empty array of the size of number_parents_crossover and the shape of the weights
    # after that we need to create an array with x number of the best parents, where x is NUMBER_PARENTS_CROSSOVER
    # inside config file. Then we search for the fittest parents inside the fitness array created by the
    # calculate_fitness function. Numpy.where return (array([], dtype=int64),) that satisfy the query, so we
    # take only the first element of the array and then it's value (the index inside fitness array). After we have
    # the index of the element we just need to take all the weights of that chromosome and insert them as a new
    # parent. Finally we change the fitness value of the fitness value of that chromosome inside the fitness
    # array in order to have all different parents and not only the fittest
    parents = numpy.empty((config.NUMBER_PARENTS_CROSSOVER, population.shape[1]))
    for parent_num in range(config.NUMBER_PARENTS_CROSSOVER):
        index_fittest = numpy.where(fitness == numpy.max(fitness))
        index_fittest = index_fittest[0][0]
        parents[parent_num, :] = population[index_fittest, :]
        fitness[index_fittest] = -999999999999
    return parents


def crossover(parents, offspring_size):
    """Create a crossover of the best parents."""
    # First we start by creating and empty array with the size equal to offspring_size we want. The type of the
    # array is [ [Index, Weights[]] ]. We select 2 random parents and then mix their weights based on a probability
    offspring = numpy.empty(offspring_size)
    for offspring_index in range(offspring_size[0]):
        while True:
            index_parent_1 = random.randint(0, parents.shape[0] - 1)
            index_parent_2 = random.randint(0, parents.shape[0] - 1)
            if index_parent_1 != index_parent_2:
                for weight_index in range(offspring_size[1]):
                    if numpy.random.uniform(0, 1) < 0.5:
                        offspring[offspring_index, weight_index] = parents[index_parent_1, weight_index]
                    else:
                        offspring[offspring_index, weight_index] = parents[index_parent_2, weight_index]
                break
    return offspring


def mutation(offspring_crossover):
    """Mutating the offsprings generated from crossover to maintain variation in the population."""
    # We mutate each genes of a chromosome based on a probability, but the range of the weights must be -1 and 1
    for offspring_index in range(offspring_crossover.shape[0]):
        for index in range(offspring_crossover.shape[1]):
            if numpy.random.random() < config.MUTATION_PERCENTAGE:
                value = numpy.random.choice(numpy.arange(-1, 1, step=0.01), size=1)
                offspring_crossover[offspring_index, index] += value
                if offspring_crossover[offspring_index, index] < -1:
                    offspring_crossover[offspring_index, index] = -1
                elif offspring_crossover[offspring_index, index] > 1:
                    offspring_crossover[offspring_index, index] = -1

    return offspring_crossover
