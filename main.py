import optparse
from os import path

import numpy
import pygame

import genetic_algorithm.genetic_algorithm as genetic_algorithm
from manager.game_manager import GameManager
from utils import config

# TODO: Fare che salvi lo snake migliore ad ogni generazione

generation_number = -1
population = numpy.random.choice(numpy.arange(-1, 1, step=0.01),
                                 size=(config.NUMBER_OF_POPULATION, config.NUMBER_WEIGHTS))

parser = optparse.OptionParser()

parser.add_option('-g', '--generation', action="store", dest="generation",
                  help="Insert the generation you would like to watch")
parser.add_option('-b', '--best-scorer', action="store", dest="best_scorer",
                  help="Insert the generation you would like to watch")

options, args = parser.parse_args()

if options.generation:
    generation_number = int(options.generation)
    if path.exists(config.WEIGHTS_FILES_FOLDER + "generation_" + str(generation_number) + "_weights.csv"):
        population = numpy.genfromtxt(
            config.WEIGHTS_FILES_FOLDER + "generation_" + str(generation_number) + "_weights.csv", delimiter=','
        )
else:
    if path.exists(config.LAST_GENERATION_FILE_NAME):
        with open(config.LAST_GENERATION_FILE_NAME, 'r') as f:
            generation_number = int(f.readline())
        if path.exists(config.WEIGHTS_FILES_FOLDER + "generation_" + str(generation_number) + "_weights.csv"):
            population = numpy.genfromtxt(
                config.WEIGHTS_FILES_FOLDER + "generation_" + str(generation_number) + "_weights.csv", delimiter=','
            )

pygame.init()
pygame.display.set_caption("Genetic Snake")
if options.best_scorer:
    if path.exists(config.BEST_SCORER_FOLDER + "generation_" + str(options.best_scorer) + "_best_scorer.csv"):
        snake = numpy.genfromtxt(
            config.BEST_SCORER_FOLDER + "generation_" + str(options.best_scorer) + "_best_scorer.csv", delimiter=','
        )
        GameManager(snake).play_game()
else:
    for _ in range(config.NUMBER_OF_GENERATION):
        generation_number += 1
        print('##############        GENERATION ', generation_number, '        ###############')
    
        snakes_fitness = genetic_algorithm.calculate_fitness(population)
        snake_fitness_copy = snakes_fitness.copy()
        print('#######  fittest chromosome in generation ', generation_number, ' is having fitness value:  ',
              numpy.max(snakes_fitness))
    
        # Selecting the best parents in the population.
        parents = genetic_algorithm.select_best_individuals(population, snakes_fitness)
        numpy.savetxt(config.BEST_SCORER_FOLDER + "generation_" + str(generation_number) + "_best_scorer.csv", parents[0],
                      delimiter=",")
        # Generating next generation using crossover.
        offspring_crossover = genetic_algorithm.crossover(parents,
                                                          offspring_size=(config.NUMBER_OF_POPULATION - parents.shape[0],
                                                                          config.NUMBER_WEIGHTS))
    
        # Adding some variations to the offspring using mutation.
        offspring_mutation = genetic_algorithm.mutation(offspring_crossover)
    
        # Creating the new population based on the parents and offspring.
        population[0:parents.shape[0], :] = parents
        population[parents.shape[0]:, :] = offspring_mutation
    
        # Saving all the data
        numpy.savetxt(config.WEIGHTS_FILES_FOLDER + "generation_" + str(generation_number) + "_weights.csv", population,
                      delimiter=",")
        numpy.savetxt(config.SCORES_FILES_FOLDER + "generation_" + str(generation_number) + "_scores.csv",
                      snake_fitness_copy, delimiter=",")
    
        with open(config.LAST_GENERATION_FILE_NAME, 'w') as f:
            f.write('%d' % generation_number)
    
    print("Calculated all the generations")
    exit(1)
