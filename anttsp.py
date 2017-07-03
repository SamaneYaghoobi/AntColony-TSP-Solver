from antcolony import AntColony
from antgraph import AntGraph
import math
import pickle
import sys
import traceback


def read_cities():
    with open("cities.txt") as f:
        content = f.read().splitlines()
    city_list = [[0 for j in range(2)] for i in range(14)]
    j = 0
    for line in content:
        city_list[j][0] = int(line[:2])
        city_list[j][1] = int(line[2:])
        j += 1
    print city_list
    paths = [[0 for j in range(14)] for i in range(14)]

    for i in range(0, 14):
        for j in range(0, 14):
            sqrt = ((city_list[i][0] - city_list[j][0]) ** 2 + (city_list[i][1] - city_list[j][1]) ** 2)
            paths[i][j] = int(math.sqrt(sqrt))

    cities = []
    for i in range(0, 14):
        cities.append('city ' + str(i + 1))

    fileobject = open("citiesAndDistances.pickled", 'wb')
    pickle.dump(cities, fileobject)
    pickle.dump(paths, fileobject)


#default
num_nodes = 14

if __name__ == "__main__":   
    if len(sys.argv) > 1 and sys.argv[1]:
        num_nodes = int(sys.argv[1])

    if num_nodes <= 10:
        num_ants = 20
        num_iterations = 12
        num_repetitions = 1
    else:
        num_ants = 28
        num_iterations = 20
        num_repetitions = 1


    stuff = pickle.load(open("citiesAndDistances.pickled", "r"))
    cities = stuff[0]
    cost_mat = stuff[1]

    if num_nodes < len(cost_mat):
        cost_mat = cost_mat[0:num_nodes]
        for i in range(0, num_nodes):
            cost_mat[i] = cost_mat[i][0:num_nodes]

    print cost_mat

    try:
        graph = AntGraph(num_nodes, cost_mat)
        best_path_vec = None
        best_path_cost = sys.maxint
        for i in range(0, num_repetitions):
            graph.reset_tau()
            ant_colony = AntColony(graph, num_ants, num_iterations)
            ant_colony.start()
            if ant_colony.best_path_cost < best_path_cost:
                best_path_vec = ant_colony.best_path_vec
                best_path_cost = ant_colony.best_path_cost

        print "\n------------------------------------------------------------"
        print "                     Results                                "
        print "------------------------------------------------------------"
        print "\nBest path = %s" % (best_path_vec,)
        for node in best_path_vec:
            print cities[node] + " --> ",
        print "Finish!"
        print "\nBest path cost = %s\n" % (best_path_cost,)
    
    except Exception, e:
        print "exception: " + str(e)
        traceback.print_exc()
