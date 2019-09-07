from utils.customer import Customer


def test_customer():
    c = Customer(1, 10, 15, 85, False)

    assert c.x == 10
    assert c.cost == 85


