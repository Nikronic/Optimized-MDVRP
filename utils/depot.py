import numpy as np
from typing import List
from copy import deepcopy

from utils.customer import Customer


class Depot:
    """
    Depot class represents a list of nodes assigned to this depot which we call a route.
    This class is going to be filled by `Customers` class.
    """

    def __init__(self, id, x, y, capacity, depot_customers: List[Customer] = None):
        """
        :param id: ID assigned to node for tracking
        :param x: X coordinate of depot
        :param y: Y coordinate of depot
        :param capacity: The maximum capacity of the Depot
        (in this project, it is filled by 'weight' of `Customers`. In other words, it indicates vehicles weight limit)
        :param depot_customers: A list of `Customer`s

        :return: A list of `Customers` assigned to this depot
        """
        if depot_customers is None:
            depot_customers = []
        self.id = id
        self.x = x
        self.y = y
        self.capacity = capacity
        self.depot_customers = depot_customers
        self.routes_ending_indices = []
        if depot_customers is not None:
            for i, c in enumerate(depot_customers):
                if c.null:
                    self.routes_ending_indices.append(i)
        self.size = self.depot_customers.__len__()

    def route_ending_index(self) -> List[int]:
        """
        Sorts then returns the list of indices corresponding to the the index of null customer representing the end
        of a route in a `Depot`.
        :return: A sorted list of ints indices
        """
        return sorted(self.routes_ending_indices)

    def used_capacity(self) -> float:
        """
        Returns a float number that demonstrates how much of the capacity of the `Depot` has been used.

        :return: A float number
        """
        return sum([customer.cost for customer in self])

    def get_all(self) -> List[Customer]:
        """
        Returns all `Customer`s as a list independently using deep copy
        :return: A list
        """
        return deepcopy(self.depot_customers)

    def add(self, customer: Customer):
        """
        Adds a `Customer` to the `Depot`
        :param customer: Customer class instance
        :return: None
        """
        if customer.null == True:
            self.routes_ending_indices.insert(self.routes_ending_indices.__len__() - 1, self.len())

        self.depot_customers.append(customer)

    def clear(self):
        """
        Clear the `Depot` from `Customer`s
        :return: None
        """
        self.routes_ending_indices = []
        self.depot_customers.clear()

    def len(self) -> int:
        """
        Return the number of `Customer`s in the `Depot`
        :return: int depot size
        """
        return self.depot_customers.__len__()

    def contains(self, customer: Customer) -> bool:
        """
        Looks for the `Customer` in the `Depot` and returns if it exist
        :param customer: A 'Customer` class instance
        :return: Bool true or false
        """
        return self.depot_customers.__contains__(customer)

    def copy(self) -> List[Customer]:
        """
        A shallow copy of the `Customer`s in the `Depot` using builtin `Copy` method
        :return: a list
        """
        return self.depot_customers.copy()

    def index(self, customer: Customer) -> int:
        """
        Returns the index of the `Customer` in the `Depot`
        :param customer: A `Customer` class instance
        :return: A int number as the index
        """
        return self.depot_customers.index(customer)

    def insert(self, index: int, customer: Customer):
        """
        Insterts a new `Customer` into a specific `index`
        :param customer: A `Customer` class instance
        :return: None
        """
        if customer.null == True:
            self.routes_ending_indices.insert(self.routes_ending_indices.__len__() - 1, index)

        return self.depot_customers.insert(index, customer)

    def remove(self, customer: Customer) -> bool:
        """
        Removes a `Customer` from the `Depot`
        :param customer: a `Customer` class instance
        :return: bool, if `Customer` does not exist returns False, else True
        """
        if self.contains(customer):
            if customer.null == True:
                self.routes_ending_indices.remove(self.index(customer))
            self.depot_customers.remove(customer)
            return True
        return False

    def remove_at(self, index: int) -> bool:
        """
        Remove a `Customer` at defined `index` from `Depot`
        :param index: an int number
        :return: bool, if `Customer` does not exist returns False, else True
        """
        if index <= self.len():
            if self.depot_customers[index].null == True:
                self.routes_ending_indices.remove(index)
            self.depot_customers.remove(self.depot_customers[index])
            return True
        return False

    def __getitem__(self, index: int):
        """
        Makes the class itself subscribable
        :param index: The index to List
        :return: A `Customer` class from List of `Customer`s.
        """
        return self.depot_customers[index]

    def describe(self, print_members=False, verbosity=False):
        """
        Print the specifics of the `Depot`

        :param print_members: Whether or not print the specifics of the `Customer`s in the `Depot`
        :param verbosity: if True, it prints all information of all members, otherwise, only IDs
        :return:
        """
        print('-=-=-=-=-=-=-=-=-=-=-=- Depot: STARTED -=-=-=-=-=-=-=-=-=-=-=-')
        if verbosity:
            print('ID:{}, coordinate=[{}, {}], capacity={}, size={}'.format(
                self.id, self.x, self.y, self.capacity, self.size))
            if print_members:
                print('Members: ')
                for c in self.depot_customers:
                    c.describe()
        else:
            print('ID={}, capacity={}/{}'.format(self.id, self.used_capacity(), self.capacity), sep='')
            print('Members IDs=')
            print([c.id for c in self])
        print('-=-=-=-=-=-=-=-=-=-=-=- Depot: Finished -=-=-=-=-=-=-=-=-=-=-=-')
