from wusn.commons import Gen, Individual, NonAnchor
import os
import math

from simulated_ToA import ToA
import common as cm
import random
from wusn.commons import  WusnInput
import numpy as np

population = []
individual_number = 0
gens = []
matrix = []
anchors = []
exact_non_anchors = []
generation = 100
selection_size = 0
result = []

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
    chromosome = individual.chromosome
    for i in range(len(chromosome)):
        indi = chromosome[i]
        non_anchors.append(NonAnchor(x=indi[0], y=indi[1], r=exact_non_anchors[i].r, order=M+i))
    for k in anchors + non_anchors:
        k.non_anchors_neighborhood(exact_non_anchors)
        # print('neibor', k.non_anchors_neibor)
        for non_an in k.non_anchors_neibor:
            d_1 = matrix[k.order][non_an.order]
            # if(d_1 != -1.):
            #     print("fuck fuck fuck")
            d_2 = cm.Euclide_distance(k.x, k.y, non_an.x, non_an.y)
            square = (d_1 - d_2)**2
            res += square
    return res

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

def mutate(individual):
    chromosome = individual.chromosome
    mean = 0.
    deviation = 1.
    child = []
    for c in chromosome:
        a = np.random.normal(mean, deviation)
        b = np.random.normal(mean, deviation)
        m, n = a + c[0], b + c[1]
        child.append([m, n])
    return Individual(child)

def to_file(path):
    with open(path, 'wt') as f:
        f.write('%d\n' % len(exact_non_anchors))
        i = len(anchors)
        for s in result.chromosome:
            f.write('%d %f %f\n' % (i, s[0], s[1]))
            i+=1

if __name__ == '__main__':
    path_1 = 'gens.test'
    path_2 = 'matrix.test'
    path_3 = ''
    # print('Enter a path to an input/output file to gens.')
    # path_1 = input()
    # print('Enter a path to an input/output file to matrix.')
    # path_2 = input()
    print('Enter a path to an input/output file to data.')
    path_3 = input()
    print(path_1)
    print(path_2)
    print(path_3)

    try:

        if not os.path.exists(path_1) or not os.path.exists(path_2) or not os.path.exists(path_3):
            print('No such path exists.')
        try:
            gens = ToA.from_file_gens(path=path_1)
            matrix = ToA.from_file_matrix(path=path_2)
            obj = WusnInput.from_file(path_3, True)
        except Exception:
            print('Failed')

        anchors = obj.anchors
        exact_non_anchors = obj.non_anchors
        init_population(80)
        individual_number = len(population)
        population.sort(key=fitness)
        selection_size = int(math.sqrt(len(population)))
        for t in range(generation):
            print(t)
            candidates = []
            while len(candidates) < selection_size:
                candidate = tournament_selection()
                candidates.append(candidate)
            for i in range(selection_size-1):
                for j in range(i+1, selection_size):
                    ch_1, ch_2 = crossover(candidates[i], candidates[j])
                    population.append(ch_1)
                    population.append(ch_2)
            for can in candidates:
                ch = mutate(can)
                population.append(ch)
            population.sort(key=fitness)
            population = population[0:individual_number]
        population.sort(key=fitness)
        result = population[0]
        to_file('result.test')
        print('res', result.chromosome)

    except (KeyboardInterrupt, EOFError):
        print()