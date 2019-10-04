from utils.customer import Customer
from utils.depot import Depot
from utils import functional as F

from typing import List
from copy import deepcopy


class Chromosome:
    """
    Chromosome data structure is a List of Lists.
    The outer scope List is `Depot`s and the inner scope List is a List of `Customer` for each `Depot`
    """

    def __init__(self, id: int, capacity: float, fitness: float = -1, chromosome: List[Depot] = None):
        """
        A empty chromosome regarding provided number of `Depot`s and capacity.
        :param id: Unique int ID for demonstration purposes
        :param capacity: The capacity of the `Depot`s which is same for all `Depot`s in a `Chromosome`
        :param chromosome: The content of the chromosome which a List of `Depot`s
        """
        if chromosome is None:
            chromosome = []
        self.id = id
        self.capacity = capacity
        for d in chromosome:
            d.capacity = self.capacity
        self.chromosome = chromosome
        self.size = self.chromosome.__len__()
        self.fitness = fitness

    def fitness_value(self) -> float:
        """
        The fitness value of the Chromosome will be calculated based on the defined criteria below:
        1. Calculate how many routes a `Chromosome` has aliased as route_count
        2. Calculate the distance in a route by summing up the distances between all members of route sequentially
            using `euclidean_distance` function aliases as distance.
        3. Fitness =  route_count + distance (note it could be weighted sum)

        :return: A float value regarding metric
        """
        distance = 0
        route_count = 0
        for depot in self:
            for route_idx in range(depot.route_ending_index().__len__()):
                route, _, _ = F.extract_route_from_depot(depot, route_idx)
                temp_depot = Customer(0, depot.x, depot.y, 0, False)
                route.insert(0, temp_depot)
                distance += sum([F.euclidean_distance(route[i - 1], route[i]) for i, _ in enumerate(route)])
                route.remove(temp_depot)
            route_count += depot.route_ending_index().__len__()
        self.fitness = distance + route_count
        return self.fitness

    def used_capacity(self) -> List[float]:
        """
        Returns a list of float number that demonstrates how much of the capacity of each `Depot` have been used.

        :return: A list of float number
        """
        return [d.used_capacity() for d in self]

    def len(self) -> int:
        """
        Number of `Depot`s in the `chromosome`
        :return: An int number
        """
        return self.chromosome.__len__()

    def get_all(self) -> List[Depot]:
        """
        Returns all `Depot`s as a list independently using deep copy
        :return: A list
        """
        return deepcopy(self.chromosome)

    def add(self, depot: Depot):
        """
        Adds a `Depot` to the `Chromosome`
        :param depot: Depot class instance
        :return: None
        """
        self.chromosome.append(depot)

    def clear(self):
        """
        Clear the `Chromosome` from `Depot`s
        :return: None
        """
        self.chromosome.clear()

    def contains(self, depot: Depot) -> bool:
        """
        Looks for the `Depot` in the `Chromosome` and returns if it exist
        :param depot: A 'Depot` class instance
        :return: Bool true or false
        """
        return self.chromosome.__contains__(depot)

    def copy(self) -> List[Depot]:
        """
        A shallow copy of the `Depot`s in the `Chromosome` using builtin `Copy` method
        :return: a list
        """
        return self.chromosome.copy()

    def index(self, depot: Depot) -> int:
        """
        Returns the index of the `Depot` in the `Chromosome`
        :param depot: A `Depot` class instance
        :return: A int number as the index
        """
        return self.chromosome.index(depot)

    def insert(self, index: int, depot: Depot):
        """
        Inserts a new `Depot` at a specific `index`
        :param index: The index of insertion
        :param depot: A `Depot` class instance
        :return: None
        """
        return self.chromosome.insert(index, depot)

    def remove(self, depot: Depot) -> bool:
        """
        Removes a `Depot` from the `Chromosome`
        :param depot: a `Depot` class instance
        :return: bool, if `Depot` does not exist returns False, else True
        """
        if self.contains(depot):
            self.chromosome.remove(depot)
            return True
        return False

    def remove_at(self, index: int) -> bool:
        """
        Remove a `Depot` at defined `index` from `Chromosome`
        :param index: an int number
        :return: bool, if `Depot` does not exist returns False, else True
        """
        if index <= self.len():
            self.chromosome.remove(self.chromosome[index])
            return True
        return False

    def __getitem__(self, index: int):
        """
        Makes the class itself subscribable
        :param index: The index to List
        :return: A `Depot` class from List of `Depot`s.
        """
        return self.chromosome[index]

    def describe(self, print_members=False, verbosity=True):
        """
        Print the specifics of the `Chromosome`

        :param print_members: Whether or not print the specifics of the `Customer`s and the `Depot`s.
        :param verbosity: if True, it prints all information of all members, otherwise, only IDs
        :return: Standard Console text
        """
        print('-=-=-=-=-=-=-=-=-=-=-=- Chromosome: STARTED -=-=-=-=-=-=-=-=-=-=-=-')
        if verbosity:
            print('ID={}, fitness={}, used capacity={}/{}, size={}'.format(
                self.id, self.fitness, self.used_capacity(), self.capacity, self.len()))
            if print_members:
                print('Members: ')
                for i, dpt in enumerate(self.chromosome):
                    print('Depot #{} Customers:'.format(i + 1))
                    for c in dpt:
                        c.describe()
        else:
            print('ID={}, fitness:{}, used capacity={}, '.
                  format(self.id, self.fitness, self.used_capacity()), sep='')
            print('Members IDs=')
            for d in self:
                print([c.id for c in d])
        print('-=-=-=-=-=-=-=-=-=-=-=- Chromosome: Finished -=-=-=-=-=-=-=-=-=-=-=-')
