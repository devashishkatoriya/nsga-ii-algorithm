
#
# Author    :   Devashish Katoriya
# Roll      :   19CS4119
#
# Program for Crowding Distance
#

from random import randint

# -------------------------------


# Function to create copy of a matrix
def copy(matrix):
    matrix2 = []
    for i in range(0, len(matrix)):
        matrix2.append(matrix[i])
    return matrix2


# Function for Sorting Pop for given objective
def sort_objective_wise(pop, fit_matrix, col=-1):
    n = len(pop)
    for i in range(0, n):
        for j in range(0, n - 1):
            if fit_matrix[j][col] > fit_matrix[j + 1][col]:
                temp = fit_matrix[j][col]
                fit_matrix[j][col] = fit_matrix[j + 1][col]
                fit_matrix[j + 1][col] = temp

                temp = pop[j]
                pop[j] = pop[j + 1]
                pop[j + 1] = temp

    return pop, fit_matrix


# Function to sort crowding distance in decending order
def sort_dec_crowding_dist(distance, pop):
    """Function to sort crowding distance in decending order

    Arguments:
        distance {[vector]} -- crowding distance vector
        pop {[2d matrix]} -- population

    Returns:
        distance -- crowding distance sorted in decreasing order
        pop -- population sorted as per crowding distance
    """

    n = len(distance)

    for i in range(0, n):
        for j in range(0, n - 1):
            if distance[j] < distance[j + 1]:
                temp = distance[j]
                distance[j] = distance[j + 1]
                distance[j + 1] = temp

                temp = pop[j]
                pop[j] = pop[j + 1]
                pop[j + 1] = temp

    return distance, pop


# Function to get maximum of a given column of fit_matrix
def get_max(fit_matrix, col=-1):
    max1 = -99999

    for i in range(0, len(fit_matrix)):
        if max1 < fit_matrix[i][col]:
            max1 = fit_matrix[i][col]

    return max1


# Function to get minimum of a given column of fit_matrix
def get_min(fit_matrix, col=-1):
    min1 = 99999

    for i in range(0, len(fit_matrix)):
        if min1 > fit_matrix[i][col]:
            min1 = fit_matrix[i][col]

    return min1


# Function to get distance for original population
def get_original_distance(pop, pop_changed, distance):
    """Function to get distance for original population

    Arguments:
        pop {[matrix]} -- original population
        pop_changed {[matrix]} -- shuffled population
        distance {[vector]} -- distance vector for shuffled population

    Returns:
        distance -- distance in correct order
    """

    distance2 = []
    done = []
    l2 = len(distance)

    for i in range(0, l2):
        done.append(False)

    for i in pop:
        for j in range(0, l2):
            if i == pop_changed[j] and done[j] == False:
                distance2.append(distance[j])
                done[j] = True
                break

    return distance2


# Function to get crowding distance of points
def crowding_distance_assignment(pop2, fit_matrix2):
    """Function to get crowding distance of solutions

    Arguments:
        pop2 {[type]} -- population from sample space
        fit_matrix2 {[type]} -- fitness matrix for 2 objectives

    Returns:
        distance2 - crowding distance for the given population
    """

    MAX = 99999
    l = len(pop2)

    pop = copy(pop2)
    fit_matrix = copy(fit_matrix2)

    # Create distance vector for each solution
    distance = []
    for i in range(0, l):
        distance.append(0)

    # For each objective m
    for i in range(0, len(fit_matrix[0])):
        pop, fit_matrix = sort_objective_wise(pop, fit_matrix, i)

        distance[0] = distance[l - 1] = MAX
        fmin1 = get_min(fit_matrix, i)
        fmax1 = get_max(fit_matrix, i)

        if fmin1 == fmax1:
            fmin1 = 0.999999
            fmax1 = 1

        for j in range(1, l - 1):
            distance[j] = distance[j] + \
                ((fit_matrix[j+1][i] - fit_matrix[j-1][i])/(fmax1 - fmin1))

    distance2 = get_original_distance(pop2, pop, distance)

    return distance2


# Main Function
def main(pop=[[0, 0]], fit_matrix=[[0, 0]]):
    """Crowding Distance Main Function

    Keyword Arguments:
        pop {2d matrix} -- population (default: {[[0, 0]]})
        fit_matrix {2d matrix} -- fitness matrix for given population (default: {[[0, 0]]})

    Returns:
        pop -- population sorted in decreasing order of crowding distance
    """

    #pop = [[16, 20], [2, 41], [93, 15], [10, 2]]
    #fit_matrix = [[16, 20], [2, 41], [93, 15], [10, 2]]

    n = len(fit_matrix)

    # Calculate crowding distance vector
    distance = crowding_distance_assignment(pop, fit_matrix)

    # Sort crowding distance vector in decreasing order
    distance, pop = sort_dec_crowding_dist(distance, pop)

    #print('Pop:', pop)
    #print('Crowding Distance:', distance)

    return pop, distance


# -------------------------------

if __name__ == "__main__":
    main()
