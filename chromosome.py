from utils.customer import Customer
from utils.depot import Depot

from typing import List
from copy import deepcopy


class Chromosome:
    """
    Chromosome data structure is a List of Lists.
    The outer scope List is `Depot`s and the inner scope List is a List of `Customer` for each `Depot`
    """

    def __init__(self, id: int, depots: int, capacity: float, fitness: float = -1, chromosome=None):
        """
        A empty chromosome regarding provided number of `Depot`s and capacity.
        :param id: Unique int ID for demonstration purposes
        :param depots: The number of `Depot`s in the chromosome
        :param capacity: The capacity of the `Depot`s which is same for all `Depot`s in a `Chromosome`
        :param chromosome: The content of the chromosome which a List of `Depot`s
        """
        if chromosome is None:
            chromosome = []
        self.id = id
        self.depots = depots
        self.capacity = capacity
        self.chromosome = chromosome
        self.size = self.chromosome.__len__()
        self.fitness = fitness

    def __fitness__(self) -> float:
        """
        The fitness value of the Chromosome based on the defined criteria in `Functions.py`
        :return: A value regarding metric
        """
        return self.fitness

    def __len__(self) -> int:
        """
        Number of `Depot`s in the chromosome
        :return: A int number
        """
        return self.chromosome.__len__()

    def __getall__(self) -> List[Depot]:
        """
        Returns all `Depot`s as a list independently using deep copy
        :return: A list
        """
        return deepcopy(self.chromosome)

    def __add__(self, depot: Depot):
        """
        Adds a `Depot` to the `Chromosome`
        :param depot: Depot class instance
        :return: None
        """
        self.chromosome.append(depot)

    def __clear__(self):
        """
        Clear the `Chromosome` from `Depot`s
        :return: None
        """
        self.chromosome.clear()

    def __contains__(self, depot: Depot) -> bool:
        """
        Looks for the `Depot` in the `Chromosome` and returns if it exist
        :param depot: A 'Depot` class instance
        :return: Bool true or false
        """
        return self.chromosome.__contains__(depot)

    def __copy__(self) -> List[Depot]:
        """
        A shallow copy of the `Depot`s in the `Chromosome` using builtin `Copy` method
        :return: a list
        """
        return self.chromosome.copy()

    def __index__(self, depot: Depot) -> int:
        """
        Returns the index of the `Depot` in the `Chromosome`
        :param depot: A `Depot` class instance
        :return: A int number as the index
        """
        return self.chromosome.index(depot)

    def __insert__(self, index: int, depot: Depot):
        """
        Inserts a new `Depot` at a specific `index`
        :param depot: A `Depot` class instance
        :return: None
        """
        return self.chromosome.insert(index, depot)

    def __remove__(self, depot: Depot) -> bool:
        """
        Removes a `Depot` from the `Chromosome`
        :param depot: a `Depot` class instance
        :return: bool, if `Depot` does not exist returns False, else True
        """
        if self.__contains__(depot):
            self.chromosome.remove(depot)
            return True
        return False

    def __remmoveat__(self, index: int) -> bool:
        """
        Remove a `Depot` at defined `index` from `Chromosome`
        :param index: an int number
        :return: bool, if `Depot` does not exist returns False, else True
        """
        if index <= self.__len__():
            self.chromosome.remove(self.chromosome[index])
            return True
        return False

    def describe(self, print_members=False):
        """
        Print the specifics of the `Chromosome`
        :param print_members: Whether or not print the specifics of the `Customer`s and the `Depot`s.
        :return:
        """
        print('ID:{}, fitness={}, capacity={}, size={}'.format(
            self.id, self.fitness, self.capacity, self.depots))
        if print_members:
            print('Members: ')
            for i, dpt in enumerate(self.chromosome):
                print('Depot #{} Customers:'.format(i+1))
                for ctmr in dpt:
                    ctmr.describe()
