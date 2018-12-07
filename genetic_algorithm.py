from wusn.commons import Gen, Individual, NonAnchor
import os
import math

from simulated_ToA import ToA
import common as cm
import random
from wusn.commons import WusnOutput, WusnInput


population = []
gens = []
matrix = []
anchors = []
exact_non_anchors = []
generation = 100
selection_size = 0

def init_population(number):
    for i in range(number):
        chromosome = []
        for g in gens:
            x, y = g.generate_chromosome()
            chromosome.append([x, y])
        population.append(Individual(chromosome))

def fitness(individual):
    res = 0
    non_anchors = []
    M = len(anchors)
    for i in range(len(individual)):
        indi = individual[i]
        non_anchors.append(NonAnchor(x=indi[0], y=indi[1], r=exact_non_anchors[i].r, order=M+i))
    for k in anchors + non_anchors:
        k.non_anchors_neighborhood(non_anchors)
        for non_an in k.non_anchors_neibor:
            d_1 = matrix[k.order][non_an.order]
            if(d_1 == -1.):
                print("fuck fuck fuck")
            d_2 = cm.Euclide_distance(k.x, k.y, non_an.x, non_an.y)
            square = (d_1 - d_2)**2
            res += square

def tournament_selection():
    individual_number = len(population)
    first = random.randint(0, individual_number-1)
    second = random.randint(0, individual_number-1)
    while second == first:
        second = random.randint(0, individual_number - 1)
    fit_1 = fitness(population[first])
    fit_2 = fitness(population[second])
    if fit_1 < fit_2:
        return population[first]
    return population[second]

def crossover(individual_1, individual_2):
    chromosome_1 = individual_1.chromosome
    chromosome_2 = individual_2.chromosome
    N = len(chromosome_1)
    cut_point = random.randint(0, N-2)
    child_1 = chromosome_1[0:cut_point+1] + chromosome_2[cut_point+1:N]
    child_2 = chromosome_2[0:cut_point+1] + chromosome_1[cut_point+1:N]
    return Individual(child_1), Individual(child_2)




if __name__ == '__main__':
    path_1 = ''
    path_2 = ''
    path_3 = ''
    print('Enter a path to an input/output file to gens.')
    input(path_1)
    print('Enter a path to an input/output file to matrix.')
    input(path_2)
    print('Enter a path to an input/output file to data.')
    input(path_3)

    try:
        while True:
            print(path_1)
            print(path_2)
            print(path_3)
            if not os.path.exists(path_1) or not os.path.exists(path_2) or not os.path.exists(path_3):
                print('No such path exists.')
                continue
            try:
                gens = ToA.from_file_gens(path_1)
                matrix = ToA.from_file_matrix(path_2)
                obj = WusnInput.from_file(path_3, True)
            except Exception:
                print('Failed')
                continue

            anchors = obj.anchors
            exact_non_anchors = obj.non_anchors
            init_population(100)
            selection_size = int(math.sqrt(len(population)))
            for _ in range(generation):
                candidates = []
                while len(candidates) < selection_size:
                    candidate = tournament_selection()
                    candidates.append(candidate)
                



    except (KeyboardInterrupt, EOFError):
        print()