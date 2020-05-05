import numpy

from utils import config

LEFT = numpy.array([-config.RECT_SIZE[0], 0])
RIGHT = numpy.array([config.RECT_SIZE[0], 0])
UP = numpy.array([0, -config.RECT_SIZE[1]])
DOWN = numpy.array([0, config.RECT_SIZE[1]])

