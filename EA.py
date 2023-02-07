import random
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Parent class
class EA:
    # Given, 
    # • Population size: 30
    # • Number of offspring to be produced in each generation :10
    # • No. of generations: 100
    # • Mutation rate: 0.5
    # • No of Iterations: 10
    def __init__(self):
        self.population_size = 30
        self.no_of_offsprings = 10
        self.no_gen = 100
        self.mutation_rate = 0.5
        self.iterations = 10
        self.fitness = None
        self.score_gen = [[] for n in range(self.no_gen)]
    
    def initialPopulation(self):
        return [[] for _ in range(self.population_size)]

    def calculate_fitness(self):
        return 0

    def mutate(self, chromosomes):
        return chromosomes

    def crossover(self, parent1, parent2):
        return parent1, parent2
    
    def cycle(self, find_max, parent_selection, survival_selection, filename):
        iters = {}
        table1 = {'Generations': [], 
                'Best Fitness so far-BSF':[],
                'Average Fitness so far-ASF':[]}
        if find_max:
            best_chromosome = [-np.inf, None]
        else:  
            best_chromosome = [np.inf, None]
        for i in range(self.iterations):
            chromosomes = self.initialPopulation() 
            # compute fitness of each individual in population
            self.fitness = [self.calculate_fitness(indv) for indv in chromosomes]
            scores = []

            for gen in range (self.no_gen):
                for _ in range(self.no_of_offsprings // 2):
                    # parent selection
                    if parent_selection == 0:
                        parents = self.fitness_proportional_selection(chromosomes, 2)
                    elif parent_selection == 1:
                        parents = self.rank_based_selection(chromosomes, 2)
                    elif parent_selection == 2:
                        parents = self.binary_tournament(chromosomes, find_max, 2)
                    elif parent_selection == 3:
                        parents = self.truncation(chromosomes, find_max, 2)
                    else:
                        parents = self.random(chromosomes, 2)
                    parent1, parent2 = parents[0], parents[1]
                    # cross over
                    offspring1, offspring2 = self.crossover(parent1, parent2)
                    # mutate offspring 
                    if random.random() < self.mutation_rate:
                        offspring1 = self.mutate(offspring1)
                        offspring2 = self.mutate(offspring2)
                    # add new offsprings to population
                    chromosomes.append(offspring1)
                    chromosomes.append(offspring2)
                    # compute fitness of new offsprings
                    self.fitness.append(self.calculate_fitness(offspring1))
                    self.fitness.append(self.calculate_fitness(offspring2))


                # survivor selection
                if survival_selection == 0:
                    chromosomes = self.fitness_proportional_selection(chromosomes, self.population_size)
                elif survival_selection == 1:
                    chromosomes = self.rank_based_selection(chromosomes, self.population_size)
                elif survival_selection == 2:
                    chromosomes = self.binary_tournament(chromosomes, find_max, self.population_size)
                elif survival_selection == 3:
                    chromosomes = self.truncation(chromosomes, find_max, self.population_size)
                else:
                    chromosomes = self.random(chromosomes, self.population_size)
                # compute fitness of each individual in population
                self.fitness = [self.calculate_fitness(indv) for indv in chromosomes]
                if find_max: 
                    # best_individual_idx = np.argmax(self.fitness)
                    BSF = max(self.fitness)
                    if BSF > best_chromosome[0]:
                        best_chromosome = [BSF, chromosomes[self.fitness.index(BSF)]]
                else: 
                    # best_individual_idx = np.argmin(np.array(self.fitness))
                    BSF = min(self.fitness)
                    if BSF < best_chromosome[0]:
                        best_chromosome = [BSF, chromosomes[self.fitness.index(BSF)]]
                # print("generations: ", gen+1, " | BSF", BSF, "| avg: ", sum(self.fitness)/len(self.fitness))

                # note readings from last iteration
                if i == self.iterations - 1:
                    table1['Generations'].append(gen+1)
                    table1['Best Fitness so far-BSF'].append(BSF)
                    table1['Average Fitness so far-ASF'].append(sum(self.fitness)/len(self.fitness))
                
                # keep record of best-so-far fitness (BSF) and average-so-far fitness (ASF)
                scores.append((BSF, sum(self.fitness)/len(self.fitness)))
            iters[i+1] = scores
            

            # maintain dictionaries for average ‘best fitness’ and average ‘average fitness’.
            table2= {'Generations': list(range(1,self.no_gen + 1)),
            'Run 1 BSF': [],
            'Run 2 BSF': [],
            'Run 3 BSF': [],
            'Run 4 BSF': [],
            'Run 5 BSF': [],
            'Run 6 BSF': [],
            'Run 7 BSF': [],
            'Run 8 BSF': [],
            'Run 9 BSF': [],
            'Run 10 BSF': [], 
            'Average BSF' : []}
            table3= {'Generations': list(range(1,self.no_gen + 1)),
            'Run 1 ASF': [],
            'Run 2 ASF': [],
            'Run 3 ASF': [],
            'Run 4 ASF': [],
            'Run 5 ASF': [],
            'Run 6 ASF': [],
            'Run 7 ASF': [],
            'Run 8 ASF': [],
            'Run 9 ASF': [],
            'Run 10 ASF': [], 
            'Average ASF' : []}
            for key, val in iters.items():
                for v in val:
                    key_name= 'Run ' + str(key) + ' BSF'
                    table2[key_name].append(v[0])
                    key_name1= 'Run ' + str(key) + ' ASF'
                    table3[key_name1].append(v[1])
                
        # calculates average BFS and average AFS
        for i in range (self.no_gen):
            sum_BSF, sum_ASF = 0, 0
            for _,val in iters.items():
                sum_BSF += val[i][0]
                sum_ASF += val[i][1]
            avg_BSF = sum_BSF / len(iters)
            avg_ASF = sum_ASF / len(iters)
            self.score_gen[i].append((avg_BSF,avg_ASF))
            table2['Average BSF'].append(avg_BSF)
            table3['Average ASF'].append(avg_ASF)

        # creating dataframes (tables)
        df1 = pd.DataFrame(table1)
        df1.to_csv('table1_' + filename + '.csv')
        df2 = pd.DataFrame(table2)
        df2.to_csv('table2_' + filename + '.csv')
        df3 = pd.DataFrame(table3)
        df3.to_csv('table3_' + filename + '.csv')
        self.plot_graph(parent_selection, survival_selection)
        return best_chromosome

    def plot_graph(self, option1, option2):
        BSF = [i[0][0] for i in self.score_gen]
        ASF = [i[0][1] for i in self.score_gen]
        generations = [i+1 for i in range(self.no_gen)]
        plt.plot(generations, BSF, label="Average best-so-far Fitness")
        plt.plot(generations, ASF, label="Average average-so-far Fitness")

        title = ''
        if option1 == 0:
            title += 'FPS and '
        elif option1 == 1:
            title += 'RBS and '
        elif option1 == 2:
            title += 'Binary Tournament and '
        elif option1 == 3:
            title += 'Truncation and '
        elif option1 == 4:
            title += 'Random and '

        if option2 == 0:
            title += 'FPS'
        elif option2 == 1:
            title += 'RBS'
        elif option2 == 2:
            title += 'Binary Tournament'
        elif option2 == 3:
            title += 'Truncation'
        elif option2 == 4:
            title += 'Random'

        plt.title(title)
        plt.xlabel('No. of generations')
        plt.ylabel('Fitness value')
        plt.legend()
        plt.show()
        

    #Selection schemes 
    def fitness_proportional_selection(self, chromosomes, size):
        # total fitness of the population/chromosomes
        total_fitness = sum(self.fitness)
        # Normalize fitness of chromosomes
        normalized_fitness = [fit_val/total_fitness for fit_val in self.fitness]
        # compute list of endpoints of ranges of fitness_val of form (start point - end point)
        start_point = 0
        ranges_endpt = []
        ranges_startpt=[]
        for i in range(len(normalized_fitness)):
            ranges_startpt.append(start_point)
            start_point += normalized_fitness[i]
            ranges_endpt.append(start_point)
            ranges_startpt.append(start_point)
        # generate two random numbers for parent 1 and parent 2
        selected_chromosomes=[]
        for i in range(size):
            rand_chromosome = random.random()
            # select chromosome if rand_parent lies in its corresponding calculated range
            for j in range (len(ranges_endpt)):
                if rand_chromosome > ranges_startpt[j] and rand_chromosome <= ranges_endpt[j]:
                    selected_chromosomes.append(chromosomes[j])
                    break
        return selected_chromosomes


    def rank_based_selection(self, chromosomes, size):
        # Assigning rank to chromosomes based on fitness values
        ranks = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i], reverse=False)
        # total of ranks of the population/chromosomes
        total_ranks = sum(ranks)
        # Normalize ranks of chromosomes
        normalized_rank = [rank_val/total_ranks for rank_val in ranks]
        # compute list of endpoints of ranges of ranks of form (start point - end point)
        start_point = 0
        ranges_endpt = []
        ranges_startpt=[]
        for i in range(len(normalized_rank)):
            ranges_startpt.append(start_point)
            start_point += normalized_rank[i]
            ranges_endpt.append(start_point)
            ranges_startpt.append(start_point)
        # generate two random numbers for parent 1 and parent 2
        selected_chromosomes =[]
        for i in range(size):
            rand_chromosome = random.random()
            # select chromosome if rand_parent lies in its corresponding calculated range
            for j in range(len(ranges_endpt)):
                if rand_chromosome > ranges_startpt[j] and rand_chromosome <= ranges_endpt[j]:
                    selected_chromosomes.append(chromosomes[j])
                    break
        return selected_chromosomes

    def binary_tournament(self, chromosomes, find_max, size):
        selected_chormosomes =[]
        selected_idx = []
        for i in range(size):
            # Choose two individuals randomly
            rand_chormosome = random.sample(range(len(chromosomes)), 2)
            if find_max:
                # Select the individual with the better fitness value
                selected_index = rand_chormosome[0] if self.fitness[rand_chormosome[0]] > self.fitness[rand_chormosome[1]] else rand_chormosome[1]
                selected_idx.append(selected_index)
            else:
                # Select the individual with the better fitness value
                selected_index = rand_chormosome[0] if self.fitness[rand_chormosome[0]] < self.fitness[rand_chormosome[1]] else rand_chormosome[1]
                selected_idx.append(selected_index)

        for i in selected_idx:
            selected_chormosomes.append(chromosomes[i])
        return(selected_chormosomes)
        

    def truncation(self, chromosomes, find_max, size):
        if find_max:
            selected_idx = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i], reverse=True)
        else:
            selected_idx = sorted(range(len(self.fitness)), key=lambda i: self.fitness[i], reverse=False)
        # selecting top ones
        selected_idx = selected_idx[:size]
        selected_chromosomes = []
        for i in selected_idx:
            selected_chromosomes.append(chromosomes[i])
        return(selected_chromosomes)


    def random(self, chromosomes, size):
        selected_chromosomes = []
        # randomly selects chromosomes from population
        selected_idx = random.sample(range(len(chromosomes)), size)
        for i in selected_idx:
            selected_chromosomes.append(chromosomes[i])
        return(selected_chromosomes)
