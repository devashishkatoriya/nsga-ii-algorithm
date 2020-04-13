
#
# Author    :   Devashish Katoriya
# Roll      :   19CS4119
#
# Program for Fast Non-Dominated Sort - Genetic Algorithm
#


import matplotlib.pyplot as plt

from random import randint

# -------------------------------


# Function to generate a single point
def generate_point(l=0, h=100):
    x = randint(l, h)
    y = randint(l, h)
    return [x, y]


# Function to generate population
def generate_pop(n=10):
    matrix = []
    for i in range(0, n):
        matrix.append(generate_point())
    return matrix


# Function to check if P1 is dominating P2
def isDominating(p1, p2):
    if p1[0] <= p2[0] and p1[1] <= p2[1]:
        return True
    return False


# Function to plot graph
def plot_graph(matrix, s):
    x = []
    y = []
    for i in range(0, len(matrix)):
        x.append(matrix[i][0])
        y.append(matrix[i][1])

    c = []
    for i in range(0, len(s)):
        c.append((s[i]+1)*3)
        s[i] = s[i] + 5
        s[i] = s[i] * 17

    plt.scatter(x, y, c=c, s=s)
    plt.show()
    return


# Function to create copy of a matrix
def copy(matrix):
    matrix2 = []
    for i in range(0, len(matrix)):
        matrix2.append(matrix[i])
    return matrix2


# Function to get dominance list and count
def get_dominance_count(pop):
    N = []
    S = []
    dBy = []

    for i in range(0, len(pop)):
        p = pop[i]
        S.append([])
        dBy.append([])
        N.append(0)
        # rank.append(-99)
        for q in pop:
            if p != q:
                if isDominating(p, q):
                    S[i].append(q)
                elif isDominating(q, p):
                    N[i] = N[i] + 1
                    dBy.append(q)
    return S, N, dBy


# Fast dominated sorting
def fast_dominated_sort(pop):

    rank = []
    Front = []
    done = []
    l = 0

    for i in range(0, len(pop)):
        Front.append(-1)
        done.append(False)
    cnt = 0

    S, N, dominatedBy = get_dominance_count(pop)
    #print('\nS:', S)
    #print('N:', N)

    while (1):
        changed = False
        N2 = copy(N)

        for i in range(0, len(N)):
            if N[i] <= 0 and done[i] == False:
                # Assign front to zero values
                Front[i] = cnt
                changed = True

                N[i] = -99
                done[i] = True

                # Change dominance count of remaining values
                for p in S[i]:
                    for j in range(0, len(pop)):
                        if pop[j] == p:
                            N2[j] = N2[j] - 1
                #print('Computed N:', N)

        # If last front
        if changed == False:
            break

        N = N2
        cnt = cnt + 1

    return Front


# Bubble sort
def sort_frontwise(matrix, fronts, pop):
    # Sort on the basis of fronts
    n = len(matrix)
    for i in range(0, n):
        for j in range(0, n - 1):
            if fronts[j] > fronts[j + 1]:
                temp = fronts[j]
                fronts[j] = fronts[j + 1]
                fronts[j + 1] = temp

                temp = matrix[j]
                matrix[j] = matrix[j + 1]
                matrix[j + 1] = temp

                temp = pop[j]
                pop[j] = pop[j + 1]
                pop[j + 1] = temp

    return matrix


# Main Function
def main(pop=[[0, 0]], fit_matrix=[[0, 0]]):
    """Main Function for Non dominated sorting

    Keyword Arguments:
        pop {2d list} -- given population (default: {[[0, 0]]})
        fit_matrix {2d list} -- fitness matrix (default: {[[0, 0]]})

    Returns:
        pop {2d list} -- frontwise sorted population
        fit_matrix {2d list} -- fitness matrix for the above
        Fronts {1d list} -- List of front for each solution 
    """
    #print('Inside Fast Non-Dominated Sort.')

    # Number of solutions
    n = 20

    # Generate population
    #pop = generate_pop(n)
    #print('\nInitial Pop:', fit_matrix)

    # Get fronts
    Fronts = fast_dominated_sort(fit_matrix)
    #print('\nFronts:', Fronts)

    # Plot graph of fronts
    #plot_graph(pop, Fronts)

    # Get front-wise sorted population
    fit_matrix = sort_frontwise(fit_matrix, Fronts, pop)
    #print('\nFinal pop:', fit_matrix)

    return pop, fit_matrix, Fronts


# -------------------------------
if __name__ == "__main__":
    main()
