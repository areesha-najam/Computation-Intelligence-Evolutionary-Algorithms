import numpy as np
import random, math
from EA import *

with open('qa194.tsp') as file:
        lines = file.readlines()
positions = []
for line in lines[7:len(lines) - 1]:
    line = line.strip('\n')
    lst = line.split(' ')
    positions.append([float(lst[1]), float(lst[2])])

class TSP(EA):
    def __init__(self):
        EA.__init__(self)
        self.totalCities = 194
        self.distances = np.zeros((194,194), dtype= int)
        for i in range (len(positions)):
            for j in range (i, len(positions)):
                self.distances[i][j] = round(math.dist(positions[i], positions[j]))
                self.distances[j][i] = self.distances[i][j] 
            
    def calculate_fitness(self, individual):
        fitness = 0

        for i in range(len(individual) - 1):
            fitness += self.distances[individual[i]][individual[i + 1]]
        fitness += self.distances[individual[-1]][individual[0]]
        return fitness

    def initialPopulation(self):
        population = np.zeros((self.population_size, self.totalCities), dtype=int)
        for i in range(self.population_size):
            population[i] = np.random.permutation(self.totalCities)
        return population.tolist()
        
    def mutate(self,individual):
        mutation_point1 = random.randint(0, len(individual) - 1)
        mutation_point2 = random.randint(0, len(individual) - 1)
        individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
        return individual

    def crossover(self, parent1, parent2):
        crossover_point = random.randint(1, len(parent1) - 1)
        child = np.zeros(len(parent1), dtype=int)
        child[:crossover_point] = parent1[:crossover_point]
        unused = np.setdiff1d(parent2, child)
        i = crossover_point
        for value in unused:
            if i == len(child):
                break
            child[i] = value
            i += 1
        return child

tsp = TSP()
# ▪ FPS and Random  
ans  = tsp.cycle(False, 0, 4)
print("FPS and Random", ans)
# ▪ Binary Tournament and Truncation 
ans  = tsp.cycle(False, 2, 3)
print("Binary Tournament and Truncation", ans)
# ▪ Truncation and Truncation 
ans  = tsp.cycle(False, 3, 3 )
print("Truncation and Truncation ", ans)
# ▪ Random and Random 
ans  = tsp.cycle(False, 4, 4)
print("Random and Random", ans)
# ▪ FPS and Truncation 
ans  = tsp.cycle(False, 0, 3)
print("FPS and Truncation", ans)
# ▪ RBS and Binary Tournament 
ans  = tsp.cycle(False, 1, 2)
print("FPS and Truncation" ,ans)
# ▪ Random and Truncation 
ans  = tsp.cycle(False, 4, 3)
print("Random and Truncation ", ans)
