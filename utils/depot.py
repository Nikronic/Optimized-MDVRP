import numpy as np
from typing import List
from copy import deepcopy

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

    def __getall__(self) -> List[Customer]:
        """
        Returns all `Customer`s as a list independently using deep copy
        :return: A list
        """
        return deepcopy(self.depot_customers)

    def __add__(self, customer: Customer):
        """
        Adds a `Customer` to the `Depot`
        :param customer: Customer class instance
        :return: None
        """
        self.depot_customers.append(customer)

    def __clear__(self):
        """
        Clear the `Depot` from `Customer`s
        :return: None
        """
        self.depot_customers.clear()

    def __len__(self):
        """
        Return the number of `Customer`s in the `Depot`
        :return: int depot size
        """
        return self.depot_customers.__len__()

    def __contains__(self, customer: Customer) -> bool:
        """
        Looks for the `Customer` in the `Depot` and returns if it exist
        :param customer: A 'Customer` class instance
        :return: Bool true or false
        """
        return self.depot_customers.__contains__(customer)

    def __copy__(self) -> List[Customer]:
        """
        A shallow copy of the `Customer`s in the `Depot` using builtin `Copy` method
        :return: a list
        """
        return self.depot_customers.copy()

    def __index__(self, customer: Customer) -> int:
        """
        Returns the index of the `Customer` in the `Depot`
        :param customer: A `Customer` class instance
        :return: A int number as the index
        """
        return self.depot_customers.index(customer)

    def __insert__(self, index: int, customer: Customer):
        """
        Insterts a new `Customer` into a specific `index`
        :param customer: A `Customer` class instance
        :return: None
        """
        return self.depot_customers.insert(index, customer)

    def __remove__(self, customer: Customer) -> bool:
        """
        Removes a `Customer` from the `Depot`
        :param customer: a `Customer` class instance
        :return: bool, if `Customer` does not exist returns False, else True
        """
        if self.__contains__(customer):
            self.depot_customers.remove(customer)
            return True
        return False

    def __remmoveat__(self, index: int) -> bool:
        """
        Remove a `Customer` at defined `index` from `Depot`
        :param index: an int number
        :return: bool, if `Customer` does not exist returns False, else True
        """
        if index <= self.__len__():
            self.depot_customers.remove(self.depot_customers[index])
            return True
        return False

    def describe(self, print_members=False):
        """
        Print the specifics of the `Depot`
        :param print_members: Whether or not print the specifics of the `Customer`s in the `Depot`
        :return:
        """
        print('ID:{}, coordinate=[{}, {}], capacity={}, size={}'.format(
            self.id, self.x, self.y, self.capacity, self.size))
        if print_members:
            print('Members: ')
            for c in self.depot_customers:
                c.describe()
