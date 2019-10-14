from utils.population import Population
from utils.customer import Customer
from utils.depot import Depot
from utils.chromosome import Chromosome

import math
import random
from copy import deepcopy
import numpy as np

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
    while i < depot.len():
        if accumulated_weight + depot[i].cost > depot.capacity:
            depot.insert(i, separator)
            accumulated_weight = 0
            i += 1
        accumulated_weight += depot[i].cost
        i += 1
    if not depot[-1].null:
        depot.add(separator)


def initialize_routing(instance) -> None:
    """
    Adds `Customer`s sequentially to the `Depot` until accumulated `weight` of `Customer`s, surpasses
    the `Depot`'s maximum `capacity.

    Note: Between two `separator` `Customer`, constructs a route to be satisfied by a vehicle.

    :param instance: An instance of `Depot`, 'Chromosome' or 'Population'
    :return: None
    """
    if instance.__class__.__name__.__contains__('Population'):
        for ch in instance:
            for d in ch:
                initial_routing(d)
    elif instance.__class__.__name__.__contains__('Chromosome'):
        for d in instance:
            initial_routing(d)
    else:
        initial_routing(instance)


# aliased in C# as "RandomList"
def randomize_customers(chromosome: Chromosome) -> None:
    """
    Randomizes all customers in all `Depot`s of the given `Chromsome` a.k.a shuffling.
    We use this method to build initial population using random `Chromosome`s.
    :param chromosome: An instance of `Chromosome` class.
    :return: None
    """
    for d in chromosome:
        random.shuffle(d.depot_customers)


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
    indices = random.sample(range(0, population.len()), size)
    new_population = Population(id=0)
    for i in indices:
        new_population.add(population[i])
    return new_population


def fittest_chromosome(population: Population) -> Chromosome:
    """
    Returns the `Chromosome` with maximum `fitness_value` within whole `Population`
    :param population: An instance of `Population` class
    :return: A single `Chromosome`
    """

    return max(population, key=lambda chromosome: chromosome.fitness_value())


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
        while first_sample == second_fittest:
            second_fittest = fittest_chromosome(second_sample)
        return Population(0, [first_fittest, second_fittest])
    else:
        indices = random.sample(range(0, first_sample.len()), 2)
        return Population(0, [first_sample[indices[0]], first_sample[indices[1]]])


def extract_random_route(chromosome: Chromosome, delete=True) -> (List[Customer], int, int, int):
    """
    Extracts a random route within a random `Depot` in given `Chromosome`.
    Note: A route defined is indicated by the `Customer`s between two `null` `Customer`s.
    :param chromosome: A `Chromosome` to be searched for route
    :param delete: Whether delete the extracted route from `Chromosome` or not.
    :return: A tuple of (List of `Customer`s, depot, start and end index)
    """
    rand_depot_index = random.randint(0, chromosome.len() - 1)
    rand_depot: Depot = chromosome[rand_depot_index]
    rand_route_idx = random.randint(0, rand_depot.route_ending_index().__len__() - 1)
    rand_route_end_idx = rand_depot.route_ending_index()[rand_route_idx]
    if rand_route_idx == 0:
        rand_route_start_idx = 0
        route = rand_depot[rand_route_start_idx: rand_route_end_idx + 1]
        if delete:
            for c in reversed(route):  # use `reversed` or we loose the `null customer` index
                rand_depot.remove(c)
        return route, rand_depot_index, rand_route_start_idx, rand_route_end_idx

    else:
        rand_route_start_idx = rand_depot.route_ending_index()[rand_route_idx - 1]
    route = rand_depot[rand_route_start_idx + 1: rand_route_end_idx + 1]
    if delete:
        for c in reversed(route):  # use `reversed` or we loose the `null customer` index
            rand_depot.remove(c)
    return route, rand_depot_index, rand_route_start_idx, rand_route_end_idx


def extract_route_from_depot(depot: Depot, route_idx: int, return_separator=False) -> (List[Customer], int, int):
    """
    Extracts a route with respect to the `route_idx` from the given `Depot`.
    Note: A route defined is indicated by the `Customer`s between two `null` `Customer`s.
    :param depot: A `Depot` to be searched
    :param route_idx: An int number representing the n'th route in `Depot`
    :param return_separator: Whether returning the `null` `Customer` as the end of route or not.
    :return: A tuple of (`List` of `Customer`s, route_start_idx, route_end_idx).
    """
    if route_idx >= depot.route_ending_index().__len__():
        raise Exception('There are not "{}" routes, try numbers between [0,{}] as "route_idx".'
                        .format(route_idx, depot.routes_ending_indices.len() - 1))
    route_end_idx = depot.route_ending_index()[route_idx]
    if route_idx == 0:
        route_start_idx = 0
        if return_separator:
            route = depot[route_start_idx: route_end_idx + 1]
            return route, route_start_idx, route_end_idx + 1
        route = depot[route_start_idx: route_end_idx]
        return route, route_start_idx, route_end_idx
    else:
        route_start_idx = depot.route_ending_index()[route_idx - 1]
        if return_separator:
            route = depot[route_start_idx + 1: route_end_idx + 1]
            return route, route_start_idx + 1, route_end_idx + 1
        route = depot[route_start_idx + 1: route_end_idx]
        return route, route_start_idx + 1, route_end_idx


def insert_customer(customer: Customer, chromosome: Chromosome) -> (int, int, int):
    """
    Inserts a `Customer` from randomly removed route of a `Depot` at a optimal place in `Chromosome`.

    The optimal place can be found using following steps:
    1. Find the nearest `Depot` to the given `Customer` using `euclidean_distance` function.
    2. Calculate the `cost` and `distance` between all members of all routes of the the chosen `Depot` from previous
       step
    3. Now the code calculates the distance in each route in the selected `Depot` if we add the `Customer` in all routes
       from index 0 to the routes' lengths. Then we add customer in the route with minimum distance regarding the
       capacity constraint on each `Depot`.
    4. Finally the code returns the index of `Depot` and the position the `Customer` has been added.

    :param customer: A `Customer` to be inserted in `Chromosome`
    :param chromosome: An instance of `Chromosome` class
    :return: A tuple of (the `Depot` index, insert index)
    """
    nearest_depot_index = int(np.argmin([euclidean_distance(customer, d) for d in chromosome]))
    nearest_depot = chromosome[nearest_depot_index]
    distances = []
    costs = []
    min_distance = 99999999  # +inf
    insert_index = -1
    route_index = -1
    depot_temp = Customer(-1, nearest_depot.x, nearest_depot.y, 0, False)  # to calculate distance between depot
    # and customers and will be removed after inserting new `Customer`

    for i in range(nearest_depot.routes_ending_indices.__len__()):
        route, _, _ = extract_route_from_depot(nearest_depot, i, False)
        route.insert(0, depot_temp)
        distances.append(sum([euclidean_distance(route[i - 1], route[i]) for i, _ in enumerate(route)]))
        costs.append(sum([c.cost for c in route]))

        if customer.cost + costs[i] <= nearest_depot.capacity:
            for ci in range(route.__len__()):
                t1 = euclidean_distance(route[ci], route[(ci + 1) % route.__len__()])
                t2 = euclidean_distance(route[ci], customer) + euclidean_distance(customer,
                                                                                  route[(ci + 1) % route.__len__()])
                t3 = distances[i] - t1 + t2

                if min_distance > t3:
                    min_distance = t3
                    route_index = i
                    insert_index = ci

        route.remove(depot_temp)

    if route_index > 0:
        insert_index += nearest_depot.route_ending_index()[route_index - 1] + 1

    if route_index == -1:
        separator = Customer(9999, nearest_depot.x, nearest_depot.y, 0, True)
        nearest_depot.add(customer)
        nearest_depot.add(separator)
        insert_index = nearest_depot.len() - 2
    else:
        nearest_depot.insert(insert_index, customer)

    return nearest_depot_index, insert_index


def cross_over(parents: Population) -> (Population, List[Customer], List[Customer]):
    """
    Gets a `Population` instance consisting of two `Chromosome`s and apply cross over on the parents based the
    following steps:
    1. First a random route need to be selected and also removed from the both `Chromosome`s
       using `extract_random_route` function. (both extraction and deletion will be done by this function)
    2. The randomly chosen route's `Customer`s from parent "1" will be added to the "second" parent using
       'insert_customer' method. Furthermore, the randomly chosen route's `Customer`s from parent "2" will be added
       to the "first" parent using aforementioned method too.

    :param parents: An instance of `Population` class with "two" `Chromosome`s
    :return: A `Population` class with "two" `Chromosome`s which has been obtained after cross-over.
    """

    first_parent, second_parent = parents[0], parents[1]
    first_route = extract_random_route(first_parent, True)[0][:-1]
    second_route = extract_random_route(second_parent, True)[0][:-1]
    for c in first_route:
        insert_customer(c, second_parent)
    for c in second_route:
        insert_customer(c, first_parent)
    crossed_parents = Population(6969, [first_parent, second_parent])
    return crossed_parents, first_route, second_route


def generate_chromosome_sample(depots: List[Depot], customers: List[Customer], out: Chromosome = None) -> Chromosome:
    """
    Gets a list of `Depot`s and `Customer`s and creates a new `Chromosome` regarding these information.
    Note: input `Depot` are only `Depot` objects and contains no `Customer` in it, so to fill those `Depot`s,
        we assign each `Customer` to its NEAREST `Depot` based on `euclidean_distance` metric.

    :param depots: A list of empty `Depot`s
    :param customers: A list of `Customer`s to be distributed between `Depot`s in the final `Chromosome`
    :param out: A `Chromosome` type object to be used instead of creating new instance. (All values will be overridden)
    :return: A filled `Chromosome`
    """
    if out is None:
        out = Chromosome(1001, depots[0].capacity, -1, depots)
    for c in customers:
        depots[int(np.argmin([euclidean_distance(c, d) for d in depots]))].add(c)
    return out


def generate_initial_population(sample: Chromosome, size: int) -> Population:
    """
    This method generates an instance of `Population` class with size of `size` and filled with `sample` `Chromosome`
    which is same. It means we will have a `Population` of cloned `Chromosome`s.

    :param sample: A `Chromosome` to be cloned and disseminated in search area
    :param size: The size of the `Population`
    :return: A `Population` instance
    """
    chromosomes = [clone(sample) for i in range(size)]
    for ch in chromosomes:
        initialize_routing(ch)
        randomize_customers(ch)
    population = Population(-6, chromosomes)
    return population


def generate_new_population(population: Population):
    """
    Generates new `Population` by crossing over winners of tournament algorithm over the whole input `Population`.
    Note: We always save the fittest for next generation, if it causes size mismatch, we remove latest new `Chromosome`.

    :param population: An initialized instance of`Population`
    :return: An evolved instance `Population`
    """

    new_population = Population(123, [fittest_chromosome(population)])
    while new_population.len() < population.len():
        crossed_parents = cross_over(tournament(population, 0.8, population.len()))
        for ch in crossed_parents:
            new_population.add(ch)
    if new_population.len() > population.len():
        new_population.remove_at(-1)
    return new_population
