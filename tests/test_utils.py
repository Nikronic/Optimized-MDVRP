import pytest
import numpy as np
from scipy.spatial import distance
import math

from population import Population
from utils.customer import Customer
from utils.depot import Depot
from chromosome import Chromosome
from utils import functional as F


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
    cb = []
    for i in range(np.random.randint(2, 10)):
        id = np.random.randint(0, 100)
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        w = np.random.randint(0, 100)
        s = False
        cb.append(Customer(id, x, y, w, s))
    return cb


def test_customer(supply_customer):
    assert supply_customer.x == 10
    assert supply_customer.cost == 85


@pytest.fixture
def supply_depot(supply_customer_batch):
    id = 0
    x = 20
    y = 30
    c = 300
    dc = supply_customer_batch
    return Depot(id, x, y, c, dc)


def test_depot_init(supply_depot):
    assert supply_depot.size >= 2
    assert supply_depot.x == 20
    assert supply_depot.depot_customers[0].x > -1
    assert supply_depot.depot_customers[0].cost > -1


def test_depot_functions(supply_depot: Depot, supply_customer: Customer):
    # __getitem__ , tests subscribable class
    assert supply_depot[0] == supply_depot.depot_customers[0]

    # __getall__
    assert supply_depot.__getall__().__len__() == supply_depot.depot_customers.__len__()

    # __add__
    l: int = supply_depot.__len__()
    supply_depot.__add__(supply_customer)
    assert supply_depot.__len__() == l + 1

    assert supply_depot.depot_customers[supply_depot.depot_customers.__len__() - 1].cost == supply_customer.cost

    # __len__
    assert supply_depot.__len__() == supply_depot.depot_customers.__len__()

    # __contains__
    assert supply_depot.__contains__(supply_customer) == True

    # __index__
    assert supply_depot.__index__(supply_customer) == supply_depot.__len__() - 1

    # __remove__
    supply_depot.__remove__(supply_customer)
    assert supply_depot.__len__() == l

    # __removeat__
    supply_depot.__remmoveat__(0)
    assert supply_depot.__len__() == l - 1
    assert supply_depot.__remmoveat__(10) == False

    # __clear__ , put it at the end of file
    supply_depot.__clear__()
    assert supply_depot.__len__() == 0


@pytest.fixture
def supply_depot_batch(supply_customer_batch):
    db = []
    for i in range(np.random.randint(2, 10)):
        id = np.random.randint(0, 100)
        x = np.random.randint(0, 100)
        y = np.random.randint(0, 100)
        c = np.random.randint(0, 100)
        db.append(Depot(id, x, y, c, supply_customer_batch))
    return db


@pytest.fixture
def supply_chromosome(supply_depot_batch):
    id = 0
    depots = supply_depot_batch.__len__()
    capacity = 500
    chromosome = supply_depot_batch
    return Chromosome(id, depots, capacity, chromosome=chromosome)


def test_chromosome_init(supply_chromosome: Chromosome):
    assert supply_chromosome.id == 0
    assert supply_chromosome.chromosome.__len__() == supply_chromosome.depots
    assert supply_chromosome.capacity == 500
    assert supply_chromosome.fitness == -1


def test_chromosome_functions(supply_chromosome: Chromosome, supply_depot: Depot):
    # __getitem__ , tests subscribable class
    assert supply_chromosome[0] == supply_chromosome.chromosome[0]

    # __fitness__
    assert supply_chromosome.__fitness__() == supply_chromosome.fitness
    assert supply_chromosome.__fitness__() == -1

    # __getall__
    assert supply_chromosome.__getall__().__len__() == supply_chromosome.chromosome.__len__()

    # __add__
    l: int = supply_chromosome.__len__()
    supply_chromosome.__add__(supply_depot)
    assert supply_chromosome.__len__() == l + 1

    assert supply_chromosome.chromosome[supply_chromosome.chromosome.__len__() - 1].capacity == supply_depot.capacity

    # __len__
    assert supply_chromosome.__len__() == supply_chromosome.chromosome.__len__()

    # __contains__
    assert supply_chromosome.__contains__(supply_depot) == True

    # __index__
    assert supply_chromosome.__index__(supply_depot) == supply_chromosome.__len__() - 1

    # __remove__
    supply_chromosome.__remove__(supply_depot)
    assert supply_chromosome.__len__() == l

    # __removeat__
    supply_chromosome.__removeat__(0)
    assert supply_chromosome.__len__() == l - 1
    assert supply_chromosome.__removeat__(10) == False

    # __clear__ , put it at the end of file before __insert__
    supply_chromosome.__clear__()
    assert supply_chromosome.__len__() == 0

    # __insert__
    supply_chromosome.__insert__(0, supply_depot)
    assert supply_chromosome.__len__() == 1


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
    l: int = supply_depot.__len__()
    F.initial_routing(supply_depot)
    assert supply_depot.__len__() >= l+1
    assert supply_depot[supply_depot.__len__()-1].null == True
    if supply_depot.__len__() >= l+2:
        assert np.sum([c.cost for c in supply_depot]) >= supply_depot.capacity


def test_randomize_customers(supply_depot):
    l: int = supply_depot.__len__()
    c = supply_depot[math.ceil(supply_depot.__len__()/2)]
    F.randomize_customers(supply_depot)
    assert supply_depot.__len__() == l
    assert supply_depot.__contains__(c) == True


def test_clone(supply_chromosome):
    cloned = F.clone(supply_chromosome)
    assert cloned != supply_chromosome
    assert cloned.__len__() == supply_chromosome.__len__()
    assert cloned.id == supply_chromosome.id
    assert cloned.capacity == supply_chromosome.capacity


@pytest.fixture
def supply_chromosome_batch(supply_depot_batch):
    chb = []
    for i in range(np.random.randint(2, 10)):
        id = np.random.randint(0, 100)
        d = np.random.randint(0, 10)
        c = np.random.randint(0, 100)
        f = np.random.randint(0, 100)
        chb.append(Chromosome(id, d, c, f, supply_depot_batch))
    return chb


@pytest.fixture
def supply_population(supply_chromosome_batch):
    id = 0
    return Population(id, supply_chromosome_batch)


def test_population_init(supply_population: Population, supply_chromosome: Chromosome):
    assert supply_population.id == 0
    assert supply_population.chromosomes.__len__() == supply_population.size


def test_population_functions(supply_population, ):
    # __getall__
    assert supply_population.__getall__().__len__() == supply_population.chromosomes.__len__()

    # __add__
    l: int = supply_population.__len__()
    supply_population.__add__(supply_chromosome)
    assert supply_population.__len__() == l + 1

    # __len__
    assert supply_population.__len__() == supply_population.chromosomes.__len__()

    # __contains__
    assert supply_population.__contains__(supply_chromosome) == True

    # __index__
    assert supply_population.__index__(supply_chromosome) == supply_population.__len__() - 1

    # __remove__
    supply_population.__remove__(supply_chromosome)
    assert supply_population.__len__() == l

    # __removeat__
    supply_population.__removeat__(0)
    assert supply_population.__len__() == l - 1
    assert supply_population.__removeat__(10) == False

    # __clear__ , put it at the end of file before __insert__
    supply_population.__clear__()
    assert supply_population.__len__() == 0

    # __insert__
    supply_population.__insert__(0, supply_chromosome)
    assert supply_population.__len__() == 1


def test_extract_population(supply_population):
    extracted = F.extract_population(supply_population, 2)
    assert extracted.__len__() == 2
    assert supply_population.__contains__(extracted[0]) == True
    assert supply_population.__contains__(extracted[1]) == True
