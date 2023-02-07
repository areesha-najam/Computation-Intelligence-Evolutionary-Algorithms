from EA import *
import random
import numpy as np

edges = {}
file = open("gcol1.txt")
for line in file.readlines()[1:-1]:
    line = line.split()
    if int(line[1]) in edges:
        edges[int(line[1])].append(int(line[2]))
    else:
        edges[int(line[1])] = []
        edges[int(line[1])].append(int(line[2]))
    
    if int(line[2]) in edges:
        edges[int(line[2])].append(int(line[1]))
    else:
        edges[int(line[2])] = []
        edges[int(line[2])].append(int(line[1]))

class GraphColoring(EA):

    def __init__(self):
        EA.__init__(self)
        self.adj_matrix = []
        self.vertices = len(edges.keys())
        self.degree =  max(edges, key=  lambda x: sum(edges[x]))

        for i in range(self.vertices):
            self.adj_matrix.append([0 for i in range(self.vertices)])
        
        for key in edges:
            for nodes in edges[key]:
                self.adj_matrix[key-1][nodes-1] = 1
                self.adj_matrix[nodes-1][key-1] = 1
        
    def initialPopulation(self)-> list:

        population = np.zeros((self.population_size, self.vertices), dtype=int)
        for i in range(self.population_size):
            np.random.seed()
            population[i] = [np.random.choice(range(self.degree)) for i in range(self.vertices)]
        return population.tolist()

    def calculate_fitness(self, chromosome):
        fitness = 0
        for i in range(self.vertices): 
            for j in range(i, self.vertices):
                # If two adjacent nodes have same color value, add a penalty to the overall fitness
                if(chromosome[i] == chromosome[j] and self.adj_matrix[i][j] == 1):
                    fitness += 1
        return fitness

    def crossover(self, parent1, parent2):
        offsprings = []
        for i in range (2):
            #  select a crossover point
            crossover_point = random.randint(1, len(parent1) - 1)
            child = np.zeros(len(parent1), dtype=int)
            #  copy bits from 0 to crossover point in child
            child[:crossover_point] = parent1[:crossover_point]
            #  populate the remaing part of child with unused values from parent2
            unused = []
            for city in parent2:
                if city not in child:
                    unused.append(city)
            i = crossover_point
            for value in unused:
                if i == len(child):
                    break
                child[i] = value
                i += 1
            offsprings.append(list(child))
        return offsprings[0], offsprings[1]

    def mutation(self, individual):
        # swap any two randomly selected bits
        mutation_point1 = random.randint(0, (len(individual)//2) - 1)
        mutation_point2 = random.randint(len(individual)//2 , len(individual) - 1)
        individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
        return individual
    
    
graph_coloring = GraphColoring()
# ▪ FPS and Random  
ans  = graph_coloring.cycle(False, 0, 4, "Graph Coloring FPS and Random")
# print("FPS and Random", ans)
# ▪ Binary Tournament and Truncation 
ans  = graph_coloring.cycle(False, 2, 3, "Graph Coloring Binary Tournament and Truncation")
# print("Binary Tournament and Truncation", ans)
# ▪ Truncation and Truncation 
ans  = graph_coloring.cycle(False, 3, 3, "Graph Coloring Truncation and Truncation ")
# print("Truncation and Truncation ", ans)
# ▪ Random and Random 
ans  = graph_coloring.cycle(False, 4, 4, "Graph Coloring Random and Random")
# print("Random and Random", ans)
# ▪ FPS and Truncation 
ans  = graph_coloring.cycle(False, 0, 3, "Graph Coloring FPS and Truncation")
# print("FPS and Truncation", ans)
# ▪ RBS and Binary Tournament 
ans  = graph_coloring.cycle(False, 1, 2, "Graph Coloring RBS and Binary Tournament")
# print("RBS and Binary Tournament" ,ans)
# ▪ Random and Truncation 
ans  = graph_coloring.cycle(False, 4, 3, "Graph Coloring Random and Truncation ")
# print("Random and Truncation ", ans)
    
        



        
