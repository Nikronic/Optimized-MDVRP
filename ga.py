from utils.chromosome import Chromosome
from utils.depot import Depot
from utils.customer import Customer
import utils.io as IO
import utils.functional as F

# Hyper-parameters
POPULATION_SIZE = 10
ITERATION = 100

# Initialization
depots, customers = IO.single_data_loader('data/input/p01', 'data/result/p01.res')
sample = F.generate_chromosome_sample(depots, customers)
population = F.generate_initial_population(sample, POPULATION_SIZE)
for ch in population:
    ch.fitness_value([1, 1])

# Iteration
for i in range(ITERATION):
    new_population = F.generate_new_population(population)
    for ch in new_population:
        ch.fitness_value()
    # describe population


