from typing import List

import pytest
import numpy as np
from scipy.spatial import distance
import math
import random

from utils.population import Population
from utils.customer import Customer
from utils.depot import Depot
from utils.chromosome import Chromosome
from utils import functional as F
import utils.io as IO


@pytest.fixture
def supply_customer():
    id = 0
    x = 10
    y = 15
    w = 85
    s = False
    return Customer(id, x, y, w, s)


@pytest.fixture
def supply_customer_batch():
    def call():
        cb = []
        for i in range(np.random.randint(2, 10)):
            id = np.random.randint(0, 100)
            x = np.random.randint(0, 100)
            y = np.random.randint(0, 100)
            w = np.random.randint(0, 100)
            s = False
            cb.append(Customer(id, x, y, w, s))
        return cb

    return call


def test_customer(supply_customer):
    assert supply_customer.x == 10
    assert supply_customer.cost == 85


@pytest.fixture
def supply_depot(supply_customer_batch):
    id = 0
    x = 20
    y = 30
    c = 200
    dc = supply_customer_batch()
    return Depot(id, x, y, c, dc)


def test_depot_init(supply_depot):
    assert supply_depot.size >= 2
    assert supply_depot.x == 20
    assert supply_depot.depot_customers[0].x > -1
    assert supply_depot.depot_customers[0].cost > -1


def test_depot_functions(supply_depot: Depot, supply_customer: Customer):
    # __getitem__ , tests subscribable class
    assert supply_depot[0] == supply_depot.depot_customers[0]

    # used_capacity
    assert supply_depot.used_capacity() > 0
    assert supply_depot.used_capacity() == sum([c.cost for c in supply_depot])

    # get_all
    assert supply_depot.get_all().__len__() == supply_depot.depot_customers.__len__()

    # add
    l: int = supply_depot.len()
    supply_depot.add(supply_customer)
    assert supply_depot.len() == l + 1

    assert supply_depot.depot_customers[supply_depot.depot_customers.__len__() - 1].cost == supply_customer.cost

    # len
    assert supply_depot.len() == supply_depot.depot_customers.__len__()

    # contains
    assert supply_depot.contains(supply_customer) == True

    # index
    assert supply_depot.index(supply_customer) == supply_depot.len() - 1

    # remove
    supply_depot.remove(supply_customer)
    assert supply_depot.len() == l

    # remove_at
    supply_depot.remove_at(0)
    assert supply_depot.len() == l - 1
    assert supply_depot.remove_at(10) == False

    # clear , put it at the end of file
    supply_depot.clear()
    assert supply_depot.len() == 0


@pytest.fixture
def supply_depot_batch(supply_customer_batch):
    def call():
        db = []
        for i in range(np.random.randint(2, 10)):
            id = np.random.randint(0, 100)
            x = np.random.randint(0, 100)
            y = np.random.randint(0, 100)
            c = np.random.randint(0, 100)
            db.append(Depot(id, x, y, c, supply_customer_batch()))
        return db

    return call


@pytest.fixture
def supply_chromosome(supply_depot_batch):
    id = 0
    capacity = 200
    chromosome = supply_depot_batch()
    return Chromosome(id=id, capacity=capacity, fitness=-1, chromosome=chromosome)


def test_chromosome_init(supply_chromosome: Chromosome):
    assert supply_chromosome.id == 0
    assert supply_chromosome.chromosome.__len__() == supply_chromosome.size
    assert supply_chromosome.capacity == 200
    assert supply_chromosome.fitness == -1


def test_chromosome_functions(supply_chromosome: Chromosome, supply_depot: Depot):
    # __getitem__ , tests subscribable class
    assert supply_chromosome[0] == supply_chromosome.chromosome[0]

    # used_capacity
    assert supply_chromosome.used_capacity()[0] == supply_chromosome[0].used_capacity()
    assert supply_chromosome.used_capacity()[-1] == supply_chromosome[-1].used_capacity()
    assert supply_chromosome.used_capacity() == [d.used_capacity() for d in supply_chromosome]

    # fitness_value
    assert supply_chromosome.fitness == -1
    F.initialize_routing(supply_chromosome)
    # file_path = "F:/Data/Github/MDVRP_UoG-master/MDVRP_UoG-master/MDVRP_UoG/MDVRP_ORIG/bin/Debug/chromosome.txt"
    # IO.chromosome_to_file(supply_chromosome, file_path)
    supply_chromosome.fitness_value()
    assert supply_chromosome.fitness == supply_chromosome.fitness_value()
    # assertion has been approved by expert and using previously implemented code.

    # get_all
    assert supply_chromosome.get_all().__len__() == supply_chromosome.chromosome.__len__()

    # add
    l: int = supply_chromosome.len()
    supply_chromosome.add(supply_depot)
    assert supply_chromosome.len() == l + 1

    assert supply_chromosome.chromosome[supply_chromosome.chromosome.__len__() - 1].capacity == supply_depot.capacity

    # len
    assert supply_chromosome.len() == supply_chromosome.chromosome.__len__()

    # contains
    assert supply_chromosome.contains(supply_depot) == True

    # index
    assert supply_chromosome.index(supply_depot) == supply_chromosome.len() - 1

    # remove
    supply_chromosome.remove(supply_depot)
    assert supply_chromosome.len() == l

    # remove_at
    supply_chromosome.remove_at(0)
    assert supply_chromosome.len() == l - 1
    assert supply_chromosome.remove_at(10) == False

    # clear , put it at the end of file before insert
    supply_chromosome.clear()
    assert supply_chromosome.len() == 0

    # insert
    supply_chromosome.insert(0, supply_depot)
    assert supply_chromosome.len() == 1


def test_euclidean_distance(supply_customer: Customer, supply_depot: Depot):
    assert F.euclidean_distance(supply_customer, supply_depot) == distance.euclidean(
        [supply_customer.x, supply_customer.y], [supply_depot.x, supply_depot.y])

    assert F.euclidean_distance(supply_customer, supply_customer) == distance.euclidean(
        [supply_customer.x, supply_customer.y], [supply_customer.x, supply_customer.y])


@pytest.fixture
def supply_separator():
    id = 0
    x = 0
    y = 0
    c = 0
    return Customer(id, x, y, c, null=True)


def test_initial_routing(supply_depot: Depot):
    l: int = supply_depot.len()
    F.initial_routing(supply_depot)
    assert supply_depot.len() >= l + 1
    assert supply_depot[-1].null == True
    if supply_depot.len() >= l + 2:
        assert np.sum([c.cost for c in supply_depot]) >= supply_depot.capacity
    for i,_ in enumerate(supply_depot):
        assert supply_depot[i-1].id != supply_depot[i]


def test_initialize_routing(supply_population, supply_chromosome, supply_depot):
    F.initialize_routing(supply_population)
    F.initialize_routing(supply_chromosome)
    F.initialize_routing(supply_depot)


def test_randomize_customers(supply_chromosome):
    di = random.randint(0, supply_chromosome.len()-1)
    l: int = supply_chromosome[di].len()
    c = supply_chromosome[di][math.ceil(supply_chromosome.len() / 2)]
    ic = supply_chromosome[di].index(c)
    F.randomize_customers(supply_chromosome)
    assert supply_chromosome[di].len() == l
    assert supply_chromosome[di].contains(c) == True


def test_clone(supply_chromosome):
    cloned = F.clone(supply_chromosome)
    assert cloned != supply_chromosome
    assert cloned.len() == supply_chromosome.len()
    assert cloned.id == supply_chromosome.id
    assert cloned.capacity == supply_chromosome.capacity


@pytest.fixture
def supply_chromosome_batch(supply_depot_batch):
    def call():
        chb = []
        for i in range(np.random.randint(2, 10)):
            id = np.random.randint(0, 100)
            c = np.random.randint(100, 200)
            f = np.random.randint(0, 100)
            chb.append(Chromosome(id, c, f, supply_depot_batch()))
        return chb

    return call


@pytest.fixture
def supply_population(supply_chromosome_batch):
    id = 0
    return Population(id, supply_chromosome_batch())


def test_population_init(supply_population: Population, supply_chromosome: Chromosome):
    assert supply_population.id == 0
    assert supply_population.chromosomes.__len__() == supply_population.size


def test_population_functions(supply_population, ):
    # get_all
    assert supply_population.get_all().__len__() == supply_population.chromosomes.__len__()

    # add
    l: int = supply_population.len()
    supply_population.add(supply_chromosome)
    assert supply_population.len() == l + 1

    # len
    assert supply_population.len() == supply_population.chromosomes.__len__()

    # contains
    assert supply_population.contains(supply_chromosome) == True

    # index
    assert supply_population.index(supply_chromosome) == supply_population.len() - 1

    # remove
    supply_population.remove(supply_chromosome)
    assert supply_population.len() == l

    # remove_at
    supply_population.remove_at(0)
    assert supply_population.len() == l - 1
    assert supply_population.remove_at(10) == False

    # clear , put it at the end of file before insert
    supply_population.clear()
    assert supply_population.len() == 0

    # insert
    supply_population.insert(0, supply_chromosome)
    assert supply_population.len() == 1


def test_extract_population(supply_population):
    extracted = F.extract_population(supply_population, 2)
    assert extracted.len() == 2
    assert supply_population.contains(extracted[0]) == True
    assert supply_population.contains(extracted[1]) == True


def test_fittest_chromosome(supply_population):
    fittest: Chromosome = F.fittest_chromosome(supply_population)
    assert supply_population.contains(fittest) == True
    for c in supply_population:
        assert fittest.fitness_value() >= c.fitness_value()


def test_tournament(supply_population):
    parents = F.tournament(supply_population)
    assert parents.len() == 2
    assert supply_population.contains(parents[0]) == True
    assert supply_population.contains(parents[1]) == True

    parents = F.tournament(supply_population, 0.0)  # force to use random parents not fittest ('else' condition)
    assert parents.len() == 2
    assert supply_population.contains(parents[0]) == True
    assert supply_population.contains(parents[1]) == True


def test_routes_ending_indices_attr(supply_depot: Depot):
    F.initial_routing(supply_depot)
    for i in supply_depot.route_ending_index():
        assert supply_depot[i].null == True
    indices = []
    for i, c in enumerate(supply_depot):
        if c.null:
            indices.append(i)
    assert sorted(indices) == (supply_depot.route_ending_index())


def test_extract_random_route(supply_chromosome):
    for d in supply_chromosome:
        F.initial_routing(d)
    route, di, si, ei = F.extract_random_route(supply_chromosome)
    for c in route:
        if not c.null:
            assert supply_chromosome[di].contains(c) == False
    assert route[-1].null == True
    for i in range(route.__len__() - 1):
        assert route[i].null == False


def test_chromosome_to_file(supply_chromosome):
    for d in supply_chromosome:
        F.initial_routing(d)
    IO.chromosome_to_file(supply_chromosome)


def test_extract_route_from_depot(supply_depot):
    F.initial_routing(supply_depot)
    route, si, ei = F.extract_route_from_depot(supply_depot,
                                               random.randint(0, supply_depot.routes_ending_indices.__len__() - 1),
                                               False)
    for c in route:
        assert supply_depot.contains(c) == True
    assert route[-1].null == False
    for _, c in enumerate(supply_depot[si: ei]):
        assert route.__contains__(c) == True
    for c in route:
        assert supply_depot[si: ei].__contains__(c) == True


def test_insert_customer(supply_chromosome):
    customer = Customer(10101010, 50, 50, 50, False)
    for d in supply_chromosome:
        F.initial_routing(d)
    # file_path = "F:/Data/Github/MDVRP_UoG-master/MDVRP_UoG-master/MDVRP_UoG/MDVRP_ORIG/bin/Debug/chromosome.txt"
    # IO.chromosome_to_file(supply_chromosome, file_path)
    di, ii = F.insert_customer(customer, supply_chromosome)
    assert supply_chromosome[di].contains(customer) == True
    assert supply_chromosome[di][ii].id == customer.id

    # Note: This is passed by another program as the ground-truth which is available in below repo
    # https://github.com/Nikronic/MDVRP_UoG/blob/master/MDVRP_UoG/MDVRP_ORIG/Test.cs


def test_cross_over(supply_population):
    parent0 = supply_population[0]
    parent1 = supply_population[1]
    for d in parent0:
        F.initial_routing(d)
    for d in parent1:
        F.initial_routing(d)
    parents = Population(0, [parent0, parent1])
    crossed_parents, route0, route1 = F.cross_over(parents)

    flag = 0
    for c in route0:
        for d in crossed_parents[1]:
            if d.contains(c):
                flag += 1
    assert flag == route0.__len__()

    flag = 0
    for c in route1:
        for d in crossed_parents[0]:
            if d.contains(c):
                flag += 1
    assert flag == route1.__len__()


# TODO: fix "file not found" error in Action
# def test_single_data_loader():
#     # test 1
#     depots, customers = IO.single_data_loader('../data/input/p01', '../data/result/p01.res')
#     assert depots[-1].id == 54 and depots[-1].x == 60 and depots[-1].y == 50 and depots[-1].capacity == 80
#     assert depots[0].id == 51 and depots[0].x == 20 and depots[0].y == 20 and depots[0].capacity == 80
#     assert depots.__len__() == 4
#
#     assert customers[-1].id == 50 and customers[-1].x == 56 and customers[-1].y == 37 and customers[-1].cost == 10
#     assert customers[0].id == 1 and customers[0].x == 37 and customers[0].y == 52 and customers[0].cost == 7
#     assert customers.__len__() == 50
#
#     # test 2
#     depots, customers = IO.single_data_loader('../data/input/p23', '../data/result/p23.res')
#     assert depots[-1].id == 369 and depots[-1].x == 110 and depots[-1].y == -110 and depots[-1].capacity == 60
#     assert depots[0].id == 361 and depots[0].x == 0 and depots[0].y == 0 and depots[0].capacity == 60
#     assert depots.__len__() == 9
#
#     assert customers[-1].id == 360 and customers[-1].x == 160 and customers[-1].y == -60 and customers[-1].cost == 1
#     assert customers[0].id == 1 and customers[0].x == -10 and customers[0].y == -10 and customers[0].cost == 12
#     assert customers.__len__() == 360
#
#     # test 3
#     depots, customers = IO.single_data_loader('../data/input/pr01', '../data/result/pr01.res')
#     assert depots[-1].id == 52 and depots[-1].x == -31.201 and depots[-1].y == 0.235 and depots[-1].capacity == 200
#     assert depots[0].id == 49 and depots[0].x == 4.163 and depots[0].y == 13.559 and depots[0].capacity == 200
#     assert depots.__len__() == 4
#
#     assert customers[-1].x == 42.883 and customers[-1].y == -2.966 and customers[-1].cost == 10
#     assert customers[0].id == 1 and customers[0].x == -29.730 and customers[0].y == 64.136 and customers[0].cost == 12
#     assert customers.__len__() == 48


def test_generate_random_sample(supply_depot_batch):
    depots: List[Depot] = supply_depot_batch()
    customers = []
    for d in depots:
        for c in d:
            customers.append(c)
        d.clear()
    chromosome = F.generate_chromosome_sample(depots, customers)
    index = int(np.argmin([F.euclidean_distance(customers[0], d) for d in depots]))
    assert chromosome[index].contains(customers[0]) == True
    index = int(np.argmin([F.euclidean_distance(customers[-1], d) for d in depots]))
    assert chromosome[index].contains(customers[-1]) == True
    assert chromosome.len() == depots.__len__()


def test_generate_initial_population(supply_chromosome):
    size = 10
    population = F.generate_initial_population(supply_chromosome, size)
    assert population.len() == size
    for i in range(population.len()):
        assert population[i-1] != population[i]
    for ch in population:
        assert ch != supply_chromosome
    for i in range(population.len()):
        assert population[i].id == supply_chromosome.id and population[i].fitness == supply_chromosome.fitness
