from chromosome import Chromosome

from typing import List
from copy import deepcopy


class Population:
    """
    A List of `Chromosome`s as a population represents different sizes.
    """
    def __init__(self, id: int, chromosomes: List[Chromosome] = None):
        """

        :param id: Unique int ID for demonstration purposes
        :param chromosomes: A `List` of `Chromosome`s
        """
        if chromosomes is None:
            chromosomes = []
        self.id = id
        self.chromosomes = chromosomes
        self.size = self.chromosomes.__len__()

    def __len__(self) -> int:
        """
        Number of `Chromosomes`s in the `Population`
        :return: An int number
        """
        return self.chromosomes.__len__()

    def __getall__(self) -> List[Chromosome]:
        """
        Returns all `Chromosome`s as a list independently using deep copy
        :return: A list
        """
        return deepcopy(self.chromosomes)

    def __add__(self, chromosome: Chromosome):
        """
        Adds a `Chromosome` to the `Population`
        :param chromosome: `Chromosome` class instance
        :return: None
        """
        self.chromosomes.append(chromosome)

    def __clear__(self):
        """
        Clear the `Population` from `Chromosome`s
        :return: None
        """
        self.chromosomes.clear()

    def __contains__(self, chromosome: Chromosome) -> bool:
        """
        Looks for the `Chromosome` in the `Population` and returns if it exist
        :param chromosome: A 'Chromosome` class instance
        :return: Bool true or false
        """
        return self.chromosomes.__contains__(chromosome)

    def __copy__(self) -> List[Chromosome]:
        """
        A shallow copy of the `Chromosome`s in the `Population` using builtin `Copy` method
        :return: a list
        """
        return self.chromosomes.copy()

    def __index__(self, chromosome: Chromosome) -> int:
        """
        Returns the index of the `Chromosome` in the `Population`
        :param chromosome: A `Chromosome` class instance
        :return: A int number as the index
        """
        return self.chromosomes.index(chromosome)

    def __insert__(self, index: int, chromosome: Chromosome):
        """
        Inserts a new `Chromosome` at a specific `index`
        :param chromosome: A `Chromosome` class instance
        :return: None
        """
        return self.chromosomes.insert(index, chromosome)

    def __remove__(self, chromosome: Chromosome) -> bool:
        """
        Removes a `Chromosome` from the `Population`
        :param chromosome: a `Chromosome` class instance
        :return: bool, if `Chromosome` does not exist returns False, else True
        """
        if self.__contains__(chromosome):
            self.chromosomes.remove(chromosome)
            return True
        return False

    def __removeat__(self, index: int) -> bool:
        """
        Remove a `Chromosome` at defined `index` from `Population`
        :param index: an int number
        :return: bool, if `Chromosome` does not exist returns False, else True
        """
        if index <= self.__len__():
            self.chromosomes.remove(self.chromosomes[index])
            return True
        return False

    def __getitem__(self, index: int) -> Chromosome:
        """
        Makes the class itself subscribable
        :param index: The index to List
        :return: A `Chromosome` class from `Population`.
        """
        return self.chromosomes[index]


