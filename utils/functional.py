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


def initial_routing(depot: Depot) -> None:
    """
    Adds `Customer`s sequentially to the `Depot` until accumulated `weight` of `Customer`s, surpasses
    the `Depot`'s maximum `capacity.

    Note: Between two `separator` `Customer`, constructs a route to be satisfied by a vehicle.
    :param depot: An instance of `Depot` class
    :return: None
    """
    accumulated_weight = 0
    separator = Customer(0, depot.x, depot.y, 0, null=True)
    for i in range(depot.__len__()):
        if accumulated_weight+depot[i].cost > depot.capacity:
            depot.__insert__(i, separator)
            accumulated_weight = 0
            i += 1
        accumulated_weight += depot[i].cost
    depot.__add__(separator)

