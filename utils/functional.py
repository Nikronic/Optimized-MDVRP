from population import Population
from utils.customer import Customer
from utils.depot import Depot
from chromosome import Chromosome

import math
import random
from copy import deepcopy

from typing import List


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
    separator = Customer(999, depot.x, depot.y, 0, True)
    i = 0
    while i < depot.__len__():
        if accumulated_weight+depot[i].cost > depot.capacity:
            depot.__insert__(i, separator)
            accumulated_weight = 0
            i += 1
        accumulated_weight += depot[i].cost
        i += 1
    # depot.__add__(separator)
    if not depot[-1].null:
        depot.__add__(separator)


# aliased in C# as "RandomList"
def randomize_customers(depot: Depot) -> None:
    """
    Randomizes all customers in a `Depot` a.k.a shuffling.
    We use this method to build initial population using random `Chromosome`s.
    :param depot: An instance of `Depot` class
    :return: None
    """
    random.shuffle(depot.depot_customers)


def clone(chromosome: Chromosome) -> Chromosome:
    """
    Clones a Chromosome with all same characteristics
    :param chromosome: An instance of `Chromosome` class to be cloned
    :return: A cloned `Chromosome`
    """

    return deepcopy(chromosome)


# aka TournamentPopulation
def extract_population(population: Population, size: int) -> Population:
    """
    Creates a shallow `Population` object with the size of `Size`.
    :param population: An instance of `Population` class
    :param size: The result `Population` size.
    :return: A `Population` class
    """
    indices = random.sample(range(0, population.__len__()), size)
    new_population = Population(id=0)
    for i in indices:
        new_population.__add__(population[i])
    return new_population


def fittest_chromosome(population: Population) -> Chromosome:
    """
    Returns the `Chromosome` with maximum `fitness` within whole `Population`
    :param population: An instance of `Population` class
    :return: A single `Chromosome`
    """

    return max(population, key=lambda chromosome: chromosome.__fitness__())


def tournament(population: Population, tournament_probability: float = 0.8, size: int = 2) -> Population:
    """
    Selects TWO parents to send them to `crossover` step based on `tournament` approach.

    Tournament approach:
    1. Select a random unique sample from the population
    2. Draw a random number; if it is below `tournament_probability` hyper-parameter do 3, else do 5
    3. Select another random unique sample from the population
    4. Find fittest chromosomes from each sampled populations and return them as new population.
    5. Randomly choose two chromosomes and return them as a new population.
    :param population: An instance of `Population` class
    :param tournament_probability: The probability of using fittest or random sample (=0.8)
    :param size: The size of population to be sampled. By default, we use Binary tournament (size = 2).
    :return: A `Population` with size of `size`
    """

    first_sample = extract_population(population, size)
    if random.random() <= tournament_probability:
        second_sample = extract_population(population, size)
        first_fittest = fittest_chromosome(first_sample)
        second_fittest = fittest_chromosome(second_sample)
        return Population(0, [first_fittest, second_fittest])
    else:
        indices = random.sample(range(0, first_sample.__len__()), 2)
        return Population(0, [first_sample[indices[0]], first_sample[indices[1]]])


def extract_random_route(chromosome: Chromosome, delete=True) -> (List[Customer], int, int, int):
    """
    Extracts a random route within a random `Depot` in given `Chromosome`.
    Note: A route defined is indicated by the `Customer`s between two `null` `Customer`s.
    :param chromosome: A `Chromosome` to be searched for route
    :param delete: Whether delete the extracted route from `Chromosome` or not.
    :return: A tuple of (List of `Customer`s, depot, start and end index)
    """
    rand_depot_index = random.randint(0, chromosome.__len__()-1)
    rand_depot: Depot = chromosome[rand_depot_index]
    rand_route_idx = random.randint(0, rand_depot.__route_ending_index__().__len__()-1)
    rand_route_end_idx = rand_depot.__route_ending_index__()[rand_route_idx]
    if rand_route_idx == 0:
        rand_route_start_idx = 0
        route = rand_depot[rand_route_start_idx: rand_route_end_idx+1]
        if delete:
            for c in reversed(route):  # use `reversed` or we loose the `null customer` index
                rand_depot.__remove__(c)
        return route, rand_depot_index, rand_route_start_idx, rand_route_end_idx

    else:
        rand_route_start_idx = rand_depot.__route_ending_index__()[rand_route_idx-1]
    route = rand_depot[rand_route_start_idx+1: rand_route_end_idx+1]
    if delete:
        for c in reversed(route):  # use `reversed` or we loose the `null customer` index
            rand_depot.__remove__(c)
    return route, rand_depot_index, rand_route_start_idx, rand_route_end_idx
