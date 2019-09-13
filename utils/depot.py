import numpy as np
from typing import List

from utils.customer import Customer

class Depot:
    """
    Depot class represents a list of nodes assigned to this depot which we call a route.
    This class is going to be filled by `Customers` class.
    """

    def __init__(self, id, x, y, capacity, depot_customers: List[Customer]) -> List[Customer]:
        """
        :param id: ID assigned to node for tracking
        :param x: X coordinate of customer
        :param y: Y coordinate of customer
        :param capacity: The maximum capacity of the Depot
        (in this project, it is filled by 'weight' of `Customers`. In other words, it indicates vehicles weight limit)
        :param depot_customers: A list of `Customer`s

        :return: A list of `Customers` assigned to this depot
        """

        self.id = id
        self.x = x
        self.y = y
        self.capacity = capacity 
        self.depot_customers = depot_customers
        self.size = len(depot_customers)

    def describe(self, print_members=False):
        print('ID:{}, coordinate=[{}, {}], capacity={}, size={}'.format(
            self.id, self.x, self.y, self.capacity, self.size))
        if print_members:
            print('Members: ')
            for c in self.depot_customers:
                c.describe()

