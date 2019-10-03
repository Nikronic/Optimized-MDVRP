from utils.customer import Customer
from utils.depot import Depot
from utils.chromosome import Chromosome
from utils.population import Population

import os
import re


def chromosome_to_file(chromosome: Chromosome, path='chromosome.txt'):
    if not os.path.exists(path):
        path = 'chromosome.txt'

    line = str(chromosome.id)+' '+str(chromosome.fitness)+' '+str(chromosome.capacity)+'\n'
    file = open(path, 'w+')
    file.write(line)

    for d in chromosome:
        line = str(d.id)+' '+str(d.x)+' '+str(d.y)+'\n'
        file.write(line)
        for c in d:
            line = str(c.id)+' '+str(c.x)+' '+str(c.y)+' '+str(c.cost)+' '+str(c.null).lower()+'\n'
            file.write(line)


def single_data_loader(input_path: str, result_path: str) -> (Population, Population):
    """
    Takes a path to input file with defined structure and create a `Population` regarding that. Also, takes the second
    path to the result file with defined structure and creates a `Population` filled with result values.

    :param input_path: Path to 'p***' files as the input
    :param result_path: Path to 'p***.res` files as the result
    :return: A tuple (`Population`: input, `Population`: desired result to be compared)
    """
    if not os.path.exists(input_path):
        raise Exception('{} does not exists.'.format(input_path))
    if not os.path.exists(result_path):
        raise Exception('{} does not exists.'.format(result_path))

    input_file = open(input_path)
    input_lines = input_file.read().split('\n')
    customer_count = int(input_lines[0].split(' ')[2])
    depot_count = int(input_lines[0].split(' ')[3])
    depot_capacities = [float(l.split(' ')[1]) for l in input_lines[1:depot_count + 1]]
    customers = []
    for line in input_lines[depot_count + 1: depot_count+customer_count + 1]:
        line = re.sub(' +', ' ', line)
        attrs = line.split(' ')
        if line[0].isspace():
            attrs = line[1:].split(' ')
        customer = Customer(int(attrs[0]), float(attrs[1]), float(attrs[2]), float(attrs[4]), False)
        customers.append(customer)

    depots = []
    for line, c in zip(input_lines[depot_count+customer_count + 1:], depot_capacities):
        line = re.sub(' +', ' ', line)
        attrs = line.split(' ')
        if line[0].isspace():
            attrs = line[1:].split(' ')
        depot = Depot(int(attrs[0]), float(attrs[1]), float(attrs[2]), c)
        depots.append(depot)

    return depots, customers
