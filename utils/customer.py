class Customer:
    """
    Customer class represents each node to be serviced by the vehicles.
    These customers is going to fll `Depot` classes.
    """

    def __init__(self, id, x, y, cost, null=False):
        """

        :param id: ID assigned to node for tracking
        :param x: X coordinate of customer
        :param y: Y coordinate of customer
        :param cost: The cost of servicing each customer
        (in this project, it is 'weight' because vehicles have weight limit)
        :param null: True if the customer is fake and used to split the list of customers as a route in each depot.

        :return:
        """

        self.id = id
        self.x = x
        self.y = y
        self.cost = cost
        self.null = null

    def describe(self):
        print('ID:{}, coordinate=[{}, {}], cost={}, separator={}'.format(
            self.id, self.x, self.y, self.cost, self.null))
