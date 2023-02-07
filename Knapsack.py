from EA import *
file_path = "instances_01_KP/low-dimensional/f8_l-d_kp_23_10000"
# n: number of items
# wmax: knapsack wmax (capacity)
# items: list of all items 
n = 0
wmax = 0
with open(file_path, 'r') as file:
    items = [(int(line.split()[0]), int(line.split()[1]), index) for index, line in enumerate(file)]
n, wmax = items[0][0], items[0][1]
items = items[1:]
# print(items, n, wmax)

class knapsack(EA):
    def __init__(self): #parentclass:EA
        EA.__init__(self)
        self.no_items = n
        self.items = items
        self.kp_capacity = wmax


    def calculate_fitness(self, offspring):
        weight, value = 0, 0
        # calculating total | weight and value picked by a chromosome
        for j in range(len(offspring)):
            if offspring[j] == 1:
                value += self.items[j][0]
                weight += self.items[j][1]
        # check if chromosome's | weight exceeds knapsack capacity (if yes then ignore)
        if weight < self.kp_capacity:
            return value
        else:
            return 0
            

    def initialPopulation(self):
        # population -> chromosomes -> genes 
        population = [[random.randint(0, 1) for i in range(self.no_items)] for j in range(self.population_size)]
        return population

    def crossover(self, parent1, parent2):
        # Choose a crossover point randomly
      
        crossover_point = random.randint(1, len(parent1)-1)

        # Create offspring by combining the genes of both parents
        offspring1 = parent1[:crossover_point] + parent2[crossover_point:]
        offspring2 = parent2[:crossover_point] + parent1[crossover_point:]
        return offspring1, offspring2

    def mutate(self,individual):
        mutation_point1 = random.randint(0, len(individual) - 1)
        mutation_point2 = random.randint(0, len(individual) - 1)
        individual[mutation_point1], individual[mutation_point2] = individual[mutation_point2], individual[mutation_point1]
        return individual

    def sum_weight(self, a):
        sum_weight = 0
        for item in range(len(a[1])):
            if a[1][item] == 1:
                sum_weight += items[item][1]
        return sum_weight

# kp = knapsack()
a = [9767, [1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0] ]
sum_ = 0
for item in range(len(a[1])):
    if a[1][item] == 1:
        print(items[item])
        sum_ += items[item][0]
print(sum)
# # ▪ FPS and Random  
# ans  = kp.cycle(True, 0, 4, "FPS and Random")
# print("FPS and Random: \n","value: ", ans[0], "|chromosome: ", ans[1], " |weight: ", kp.sum_weight(ans))
# # ▪ Binary Tournament and Truncation 
# ans  = kp.cycle(True, 2, 3, "Binary Tournament and Truncation")
# print("Binary Tournament and Truncation: \n"," value: ", ans[0],"|chromosome: ", ans[1], " |weight: ",  kp.sum_weight(ans))
# # ▪ Truncation and Truncation 
# ans  = kp.cycle(True, 3, 3, "Truncation and Truncation ")
# print("Truncation and Truncation: \n","value: ", ans[0], "|chromosome: ", ans[1], " |weight: ", kp.sum_weight(ans))
# # ▪ Random and Random 
# ans  = kp.cycle(True, 4, 4, "Random and Random")
# print("Random and Random: \n","value: ", ans[0], "|chromosome: ", ans[1], " |weight: ", kp.sum_weight(ans))
# # ▪ FPS and Truncation 
# ans  = kp.cycle(True, 0, 3, "FPS and Truncation")
# print("FPS and Truncation: \n","value: ", ans[0], "|chromosome: ", ans[1], " |weight: ", kp.sum_weight(ans))
# # ▪ RBS and Binary Tournament 
# ans  = kp.cycle(True, 1, 2, "RBS and Binary Tournament")
# print("RBS and Binary Tournament: \n", "value: ", ans[0], "|chromosome: ", ans[1], " |weight: ", kp.sum_weight(ans))
# # ▪ Random and Truncation 
# ans  = kp.cycle(True, 4, 3, "Random and Truncation ")
# print("Random and Truncation: \n", "value: ", ans[0], "|chromosome: ", ans[1], " |weight: ", kp.sum_weight(ans))



















