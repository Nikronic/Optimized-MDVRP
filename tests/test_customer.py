import pytest
import numpy as np
from utils.customer import Customer


@pytest.fixture
def supply_customer():
    id = np.random.randint(1, 100)
    x = np.random.randint(1, 100)
    y = np.random.randint(1, 100)
    w = np.random.randint(1, 100)
    s = (np.random.rand(1) > 0.5)[0]
    return Customer(id, x, y, w, s)


def test_customer():
    c = supply_customer()
    assert c.x == 10
    assert c.cost == 85
