import math
from numpy import random
import time
from collections.abc import Iterable
import csv

def fitness(sequence, evaluator):
    result = evaluator.run(sequence)
    res = result[0][0]
    return res

def softmax(lst):
    result = []
    lst = list(map(math.exp, lst))
    sigma = sum(lst)
    for value in lst:
        result.append(value/sigma)
    return result

def fitnesses(population, best_value, evaluator, fitness_step):
    result = []
    for sequence in population:
        temp_value = fitness(sequence, evaluator)
        result.append(temp_value)
        if temp_value > best_value:
            best_value = temp_value
        fitness_step += 1
    return result, fitness_step

def mutation(parameter, mutation_rate):
    if isinstance(parameter, Iterable):
        result = []
        for i in parameter:
            result.append(mutation(i, mutation_rate))
    else:
        if random.random() < mutation_rate:
            result = random.randint(0, 20)
        else:
            result = parameter
    return result

def step(population, fitnesses_result, population_size, mutation_rate):
    numbers = len(population[0])
    indexes = list(range(0, len(population)))
    roulette = softmax(fitnesses_result)
    new_population = []
    for i in range(population_size):
        parents_index1, parents_index2 = random.choice(indexes, p=roulette), random.choice(indexes, p=roulette)
        parents_1, parents_2 = population[parents_index1], population[parents_index2]
        crossover = random.randint(0, numbers + 1)
        offspring = parents_1[:crossover] + parents_2[crossover:]
        offspring = mutation(offspring, mutation_rate)
        new_population.append(offspring)
    return new_population    

def ga(population, mutation_rate, evaluator, fitness_step):
    start = time.time()
    f = open('result.csv', 'w')
    wr = csv.writer(f)
    generation_step = 0
    best_value = 0
    population_size = len(population)
    total_population_size = 0
    fitnesses_result, fitness_step = fitnesses(population, best_value, evaluator, fitness_step)
    best_index = fitnesses_result.index(max(fitnesses_result))
    best_value = fitnesses_result[best_index]
    best_input = population[best_index]
    if best_value >= 1.0:
        f.close()
        return best_input, best_value, fitness_step, total_population_size
    while time.time() - start <= 400:
    # while population_size <= 80000:
        population = step(population, fitnesses_result, population_size, mutation_rate)
        total_population_size += population_size
        fitnesses_result, fitness_step = fitnesses(population, best_value, evaluator, fitness_step)
        best_index = fitnesses_result.index(max(fitnesses_result))
        if fitnesses_result[best_index] > best_value:
            best_value = fitnesses_result[best_index]
            best_input = population[best_index]
        if total_population_size % 200 == 0:
            print('population size = {}, best_value = {}'.format(total_population_size, best_value))
            # wr.writerow([total_population_size, best_value])
        wr.writerow([time.time() - start, best_value])
        if best_value >= 1.0:
            f.close()
            return best_input, best_value, fitness_step, total_population_size
        generation_step += 1
    f.close()
    return best_input, best_value, fitness_step, total_population_size

def main(population, mutation_rate, evaluator):
    start = time.time()
    best_input, best_value, fitness_step, total_population_size= ga(population, mutation_rate, evaluator, 0)
    running_time = time.time() - start
    return best_input, best_value, fitness_step, total_population_size, running_time
