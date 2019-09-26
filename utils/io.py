from utils.customer import Customer
from utils.depot import Depot
from chromosome import Chromosome


def chromosome_to_file(chromosome: Chromosome, path='chromosome.txt'):
    line = str(chromosome.id)+' '+str(chromosome.fitness)+' '+str(chromosome.capacity)+'\n'
    file = open(path, 'w+')
    file.write(line)

    for d in chromosome:
        line = str(d.id)+' '+str(d.x)+' '+str(d.y)+'\n'
        file.write(line)
        for c in d:
            line = str(c.id)+' '+str(c.x)+' '+str(c.y)+' '+str(c.cost)+' '+str(c.null).lower()+'\n'
            file.write(line)
