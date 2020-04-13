
#
# Author    :   Devashish Katoriya
# Roll      :   19CS4119
#
# Program to implement NSGA - II
#


import matplotlib.pyplot as plt
import fnsa
import crowding_distance

from random import random
from random import randint


# ---------------------------------------


# Function to generate initial population randomly
def init_pop(matrix, pop, n):

    for i in range(0, pop):
        chromosome = []
        for j in range(0, n):
            val = randint(0, n-1)
            while val in chromosome:
                val = randint(0, n-1)
            chromosome.append(val)
        matrix.append(chromosome)

    return matrix


# Function for evaluating fitness
def get_fitness(arr, cost):
    dist = 0
    prev = arr[0]
    for i in range(1, len(arr)):
        dist = dist + cost[prev][arr[i]]
    dist = dist + cost[arr[len(arr)-1]][arr[0]]
    return dist


# Function for evaluating fitness of total matrix
def get_overall_fitness(matrix, cost):
    fitness = 0
    for i in range(0, len(matrix)):
        fitness = fitness + get_fitness(matrix[i], cost)
    return fitness


# Function to perform mutation
def mutate(matrix, um, n):

    pop = len(matrix)
    for i in range(0, pop):
        chance = random()               # Chance that mutation will occur
        if chance < um:
            pos = randint(0, n - 1)
            val = matrix[i][pos]
            matrix[i][pos], matrix[i][val] = matrix[i][val], matrix[i][pos]

    return matrix


# Function to perform crossover over two chromosomes
def crossover(chrome1, chrome2):

    # We're using Order1 Crossover
    children = []
    l = len(chrome1)

    # create blank children
    for i in range(0, l):
        children.append([])
        for j in range(0, l):
            children[i].append(-1)

    # Run for 2 children
    for k in range(0, 2):

        # create interval to keep
        pos1 = randint(0, l - 1)
        pos2 = randint(0, l - 1)

        # If upper limit is lower than lower limit
        if pos2 < pos1:
            pos1, pos2 = pos2, pos1

        # First copy interval range as it is
        for i in range(pos1, pos2+1):
            children[k][i] = chrome1[i]

        # Now crossover left side
        i = 0
        while i < pos1:
            j = 0
            while chrome2[j] in children[k] and j < l:
                j = j + 1
            children[k][i] = chrome2[j]
            i = i + 1

        # Similarly crossover right side
        i = pos2 + 1
        while i < l:
            j = 0
            while chrome2[j] in children[k] and j < l:
                j = j + 1
            children[k][i] = chrome2[j]
            i = i + 1

    return children[0], children[1]


# Utility function for performing crossover
def perform_crossover(matrix, uc):

    matrix2 = []

    pop = len(matrix)
    i = 0
    while i < pop - 1:
        chance = random()

        if chance <= uc:
            child1, child2 = crossover(matrix[i], matrix[i + 1])
        else:
            child1, child2 = matrix[i], matrix[i + 1]

        matrix2.append(child1)
        matrix2.append(child2)

        i = i + 2

    return matrix2


# Function to perform selection based on fitness value
def selection(chrome1, chrome2, cost, time):

    # Fitness value of chromosome 1
    f1 = get_fitness(chrome1, cost)
    f1 = f1*f1 * get_fitness(chrome1, time)

    # Fitness value of chromosome 2
    f2 = get_fitness(chrome2, cost)
    f2 = f2*f2 * get_fitness(chrome2, time)

    if f1 < f2:
        return chrome1
    else:
        return chrome2


# Utility function for selection operator
def perform_selection(matrix, cost, time):

    pop = len(matrix)
    matrix2 = []

    for i in range(0, pop):
        val1 = randint(0, pop-1)
        val2 = randint(0, pop-1)

        matrix2.append(selection(matrix[val1], matrix[val2], cost, time))

    return matrix2


# Function to get pair of fitness values
def combined_fitness(arr, c1, c2):
    f1 = get_fitness(arr, c1)
    f2 = get_fitness(arr, c2)

    return [f1, f2]


# Function to get pair of fitness values in matrix form
def combined_overall_fitness(matrix, c1, c2):
    fit_matrix = []
    for i in range(0, len(matrix)):
        fit_matrix.append(combined_fitness(matrix[i], c1, c2))

    return fit_matrix


# Function to create upper half
def take_first_half(matrix, fit_matrix, Fronts):

    matrix2 = []
    n = len(Fronts)
    mid = int(n/2)

    fm = Fronts[mid]

    # Copy upper matrix as it is
    i = 0
    while (Fronts[i] != fm):
        matrix2.append(matrix[i])
        i = i + 1

    # Create sub-matrix for crowding distance
    beg = i
    while (i < n and Fronts[i] == fm):
        i = i + 1
    end = i

    pop2 = []
    fit_matrix2 = []
    for j in range(beg, end):
        pop2.append(matrix[j])
        fit_matrix2.append((fit_matrix[j]))

    # Get sub-matrix sorted as per crowding distance
    pop2, distance = crowding_distance.main(pop2, fit_matrix)

    # Copy remaining population from sub-matrix
    i = beg
    while i < mid:
        matrix2.append(pop2[i - beg])
        i = i + 1

    #print('Len matrix:', len(matrix))
    #print('Len matrix2:', len(matrix2))

    return matrix2


# Function to join two matrices
def combine_matrices(matrix, matrix2):
    matrix3 = []
    for i in range(0, len(matrix)):
        matrix3.append(matrix[i])
    for i in range(0, len(matrix2)):
        matrix3.append(matrix2[i])

    return matrix3


# Function to plot graph
def plot_graph(pop, cost, time, cnt=1):
    X = []
    Y = []
    #color = []

    fit_matrix = combined_overall_fitness(pop, cost, time)
    #print('Final Fitness Matrix:', fit_matrix)
    n = len(fit_matrix)

    for i in range(0, n):
        X.append(fit_matrix[i][0])
        Y.append(fit_matrix[i][1])
        # color.append(cnt)

    plt.scatter(X, Y)
    # plt.show()

    return


# Function to import csv file into matrix
def import_csv(filename):
    matrix = []
    k = 0
    file1 = open(filename, 'r')
    for line in file1.readlines():
        data1 = line.split(',')
        matrix.append([])
        for val in data1:
            matrix[k].append(float(val))
        k = k + 1

    return matrix


# Main Function
def main():
    pop = 50            # Population size
    uc = 0.9            # Crossover rate
    um = 0.1            # Mutation rate
    l = 30              # Number of Iterations
    MAX = 9999          # Infinite

    n = 5               # Number of Cities
    cost = [[0, 2, MAX, 12, 5],
            [2, 0, 4, 8, MAX],
            [MAX, 4, 0, 3, 3],
            [12, 8, 3, 0, 10],
            [5, MAX, 3, 10, 0]]

    time = [[0, 6, MAX, 9, 8],
            [6, 0, 3, 5, MAX],
            [MAX, 3, 0, 2, 7],
            [9, 5, 2, 0, 4],
            [8, MAX, 7, 4, 0]]

    cost = [[0, 81, 72, 55, 81, 3],
            [81, 0, 3, 44, 99, 40],
            [72, 3, 0, 87, 72, 21],
            [55, 44, 87, 0, 67, 25],
            [81, 9, 77, 67, 0, 93],
            [3, 40, 21, 25, 93, 0]]

    time = [[0, 82, 14, 14, 43, 47],
            [82, 0, 61, 76, 29, 47],
            [14, 61, 0, 29, 31, 51],
            [14, 76, 29, 0, 78, 67],
            [43, 29, 31, 78, 0, 28],
            [47, 47, 51, 67, 28, 0]]

    n = len(time)

    cost = import_csv('distances.csv')
    time = import_csv('time2.csv')
    n = len(time)

    fitness = []
    matrix = []

    while (1):

        # Initial Population
        matrix = init_pop(matrix, pop, n)

        # Perform Selection
        matrix = perform_selection(matrix, cost, time)

        for i in range(0, l):
            print('\nIte: #', i + 1)

            #print('Pop:', matrix)

            # Create Pop: P
            matrix2 = fnsa.copy(matrix)

            # Create Pop: Q
            # Perform Crossover
            matrix = perform_crossover(matrix, uc)

            # Perform Mutation
            matrix = mutate(matrix, um, n)

            # Join P and Q
            matrix = combine_matrices(matrix, matrix2)

            # Calculate fitness
            fit_matrix = combined_overall_fitness(matrix, cost, time)

            # Fast non-dominated sort
            matrix, fit_matrix, Fronts = fnsa.main(matrix, fit_matrix)

            # Create back Q
            matrix = take_first_half(matrix, fit_matrix, Fronts)

            # Termination condition
            # if tsp_ga.get_fitness(matrix[1], cost) <= threshold:
            #    break

            # Plot graph of fitness values over the generations
            #plot_graph(matrix, cost, time, i)

            #print('Fronts:', Fronts)

        #print('Final population:', matrix)

        plot_graph(matrix, cost, time, i)
        #plt.ylim(ymin=1400, ymax=2400)
        #plt.xlim(xmin=11000, xmax=17000)
        plt.show()

        #choice2 = input("\n\nDo you want to continue (y/n) ? ")
        choice2 = 'n'
        if choice2 != "y":
            print("\n\nThank you!")
            break

    return


# ---------------------------------------

if __name__ == "__main__":
    main()
