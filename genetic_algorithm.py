from wusn.commons import Gen, Individual, NonAnchor
import os

from wusn.commons import WusnOutput, WusnInput
from simulated_ToA import ToA


population = []
gens = []

def init_population(number):
    for i in range(number):
        chromosome = []
        for g in gens:
            x, y = g.generate_chromosome()
            chromosome.append([x, y])
        population.append(Individual(chromosome))

def fitness(individual, anchors, non_anchor_radius):
    res = 0
    non_anchors = []
    M = len(anchors)
    for i in range(len(individual)):
        indi = individual[i]
        non_anchors.append(NonAnchor(x=indi[0], y=indi[1], r=non_anchor_radius, order=M+i))
    # for k in anchors:
    #     k.non_anchors_neighborhood(non_anchors)
    #     for non_an in k.non_anchors_neibor:
    #         res +=

if __name__ == '__main__':
    path_1 = ''
    path_2 = ''
    print('Enter a path to an input/output file to gens.')
    input(path_1)
    print('Enter a path to an input/output file to matrix.')
    input(path_2)

    try:
        while True:
            print(path_1)
            print(path_2)
            if not os.path.exists(path_1) :
                print('No such path exists.')
                continue
            try:
                gens = ToA.from_file_gens(path_1)
                matrix = ToA.from_file_matrix(path_2)
            except Exception:
                print('Failed')
                continue

            init_population(100)



    except (KeyboardInterrupt, EOFError):
        print()