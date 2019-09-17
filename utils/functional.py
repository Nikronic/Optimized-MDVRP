from utils.customer import Customer
from utils.depot import Depot
from chromosome import Chromosome

import math


def euclidean_distance(source: Customer, target) -> float:
    """
    Computes the Euclidean Distance between two (x, y) coordinates
    :param source: An instance of `Customer` or `Depot` class
    :param target: An instance of `Customer` or `Depot` class
    :return: A float number
    """
    return math.sqrt(math.pow(source.x - target.x, 2) + math.pow(source.y - target.y, 2))




