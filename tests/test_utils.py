import pytest
import numpy as np
from utils.customer import Customer
from utils.depot import Depot


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
        s = np.random.randint(0, 100) > 50
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
    c = 500
    dc = supply_customer_batch
    return Depot(id, x, y, c, dc)


def test_depot_init(supply_depot):
    assert supply_depot.size >= 2
    assert supply_depot.x == 20
    assert supply_depot.depot_customers[0].x > -1
    assert supply_depot.depot_customers[0].cost > -1


def test_depot_functions(supply_depot: Depot, supply_customer: Customer):
    # __getall__
    assert supply_depot.__getall__().__len__() == supply_depot.depot_customers.__len__()

    # __add__
    l = supply_depot.__len__()
    supply_depot.__add__(supply_customer)
    assert supply_depot.__len__() == l+1

    assert supply_depot.depot_customers[supply_depot.depot_customers.__len__()-1].cost == supply_customer.cost

    # __len__
    assert supply_depot.__len__() == supply_depot.depot_customers.__len__()

    # __contains__
    assert supply_depot.__contains__(supply_customer) == True

    # __index__
    assert supply_depot.__index__(supply_customer) == supply_depot.__len__()-1

    # __remove__
    supply_depot.__remove__(supply_customer)
    assert supply_depot.__len__() == l

    # __removeat__
    supply_depot.__remmoveat__(0)
    assert supply_depot.__len__() == l-1
    assert supply_depot.__remmoveat__(10) == False

    # __clear__ , put it in as the last test
    supply_depot.__clear__()
    assert supply_depot.__len__() == 0




