import numpy

from utils import config


def soft_max(z):
    return numpy.exp(z.T) / numpy.sum(numpy.exp(z.T), axis=1).reshape(-1, 1)


def sigmoid(z):
    return 1 / (1 + numpy.exp(-z))


def relu(z):
    return numpy.maximum(0, z)


class NeuralNetwork:
    """Class that represent the Neural Network."""

    def __init__(self, weights):
        self.__input_values = numpy.empty(shape=(1, config.INPUT))
        self.__weights = weights
        self.__W1_shape = (config.NEURONS_HIDDEN_1, config.INPUT)
        self.__W2_shape = (config.OUTPUT, config.NEURONS_HIDDEN_1)
        self.__W1 = self.__weights[0:self.__W1_shape[0] * self.__W1_shape[1]].reshape(self.__W1_shape[0], self.__W1_shape[1])
        self.__W2 = self.__weights[self.__W1_shape[0] * self.__W1_shape[1]:].reshape(self.__W2_shape[0], self.__W2_shape[1])

    def update_parameters(self, vision):
        """Update all the input values of the Neural Network."""
        self.__input_values = vision.reshape(-1, config.INPUT)

    def forward_propagation(self):
        """Propagates the initial information to the hidden units at each layer and finally produce the output."""
        z1 = numpy.matmul(self.__W1, self.__input_values.T)
        a1 = relu(z1)
        z2 = numpy.matmul(self.__W2, a1)
        a2 = soft_max(z2)
        return a2

    def get_action(self):
        """Based on the output of the forward_propagation produce an Action."""
        # Index max represent the index of the max value of the forward_propagation
        # after that we use that index to create an action based on the snake orientation. So, first, we get his
        # orientation, than we create the correct action based on it.
        return numpy.argmax(numpy.array(self.forward_propagation()))
