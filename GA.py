import math
from numpy import random
import time
from collections.abc import Iterable
from Mutants.mutating_tester import get_mutation_score
from tester import Tester

def fitness(sequence, fun_name):
    # todo
    tester = Tester()
    tester.reset(argnum=3, max_value=20, condition_range=5, error_rate=0.3, correction_range=[])
    result = tester.run(sequence)
    res = result[0][0]
    # mutation_score = get_mutation_score(fun_name, sequence)
    return res

def softmax(lst):
    result = []
    sigma = sum(lst)
    if sigma == 0:
        for _ in range(len(lst)):
            result.append(1/len(lst))
    else:
        for value in lst:
            result.append(value/sigma)
    return result

def fitnesses(population, best_value, fun_name, fitness_step):
    result = []
    for sequence in population:
        temp_value = fitness(sequence, fun_name)
        result.append(temp_value)
        if temp_value > best_value:
            best_value = temp_value
        fitness_step += 1
        if fitness_step % 100 == 0:
            print('fitness step = {}, best_value = {}'.format(fitness_step, best_value))
    return result, fitness_step

def mutation(parameter, fun_name, mutation_rate):
    if fun_name == "get_factors" or fun_name == "quicksort":
        if isinstance(parameter, Iterable):
            result = []
            for i in parameter:
                result.append(mutation(i, fun_name, mutation_rate))
        else:
            if fun_name == "get_factors":
                if random.random() < mutation_rate:
                    result = random.randint(0, 10000) # constraints for get_factors
                else:
                    result = parameter
            else:
                if random.random() < mutation_rate:
                    result = random.randint(0, 100) # constraints for quicksort
                else:
                    result = parameter
    elif fun_name == "hanoi":
        result = []
        for input_pair in parameter:
            mutated_input = []
            for i in range(3):
                if random.random() < mutation_rate:
                    # constraints for hanoi
                    if i == 0:
                        mutated_input.append(random.randint(0, 20))
                    elif i == 1:
                        mutated_input.append(random.randint(1, 3))
                    elif i == 2:
                        mutated_input.append(random.randint(1, 3))
                        while mutated_input[1] == mutated_input[2]:
                            mutated_input[2] = random.randint(1, 3)
                    # constraints for hanoi
                else:
                    mutated_input.append(input_pair[i])
            result.append(mutated_input)
    elif fun_name == "knapsack": # constraints for knapsack
        result = []
        for input_pair in parameter:
            mutated_input = []
            if random.random() < mutation_rate:
                mutated_input.append(random.randint(0, 100))
            else:
                mutated_input.append(input_pair[0])
            items = []
            for item in input_pair[1]:
                mutated_item = []
                if random.random() < mutation_rate:
                    mutated_item.append(random.randint(0, 100))
                else:
                    mutated_item.append(input_pair[0])
                if random.random() < mutation_rate:
                    mutated_item.append(random.randint(0, 10))
                else:
                    mutated_item.append(input_pair[0])
                items.append(mutated_item)
            mutated_input.append(items)
            result.append(mutated_input)
    return result


def step(population, fitnesses_result, population_size, fun_name, mutation_rate):
    numbers = len(population[0])
    indexes = list(range(0, len(population)))
    roulette = softmax(fitnesses_result)
    new_population = []
    for i in range(population_size):
        parents_index1, parents_index2 = random.choice(indexes, p=roulette), random.choice(indexes, p=roulette)
        parents_1, parents_2 = population[parents_index1], population[parents_index2]
        crossover = random.randint(0, numbers + 1)
        offspring = parents_1[:crossover] + parents_2[crossover:]
        offspring = mutation(offspring, fun_name, mutation_rate)
        new_population.append(offspring)
    return new_population    

def ga(population, mutation_rate, fun_name, fitness_step):
    generation_step = 0
    best_value = 0
    population_size = len(population)
    total_population_size = population_size
    fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
    best_index = fitnesses_result.index(max(fitnesses_result))
    best_value = fitnesses_result[best_index]
    best_input = population[best_index]
    if best_value >= 1.0:
        return best_input, best_value, fitness_step, total_population_size
    while generation_step < 25000:
        population = step(population, fitnesses_result, population_size, fun_name, mutation_rate)
        total_population_size += population_size
        fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
        best_index = fitnesses_result.index(max(fitnesses_result))
        if fitnesses_result[best_index] > best_value:
            best_value = fitnesses_result[best_index]
            best_input = population[best_index]
        if total_population_size % 10 == 0:
            print('population size = {}, best_value = {}'.format(total_population_size, best_value))
        if best_value >= 1.0:
            return best_input, best_value, fitness_step, total_population_size
        generation_step += 1
    return best_input, best_value, fitness_step, total_population_size

def main(population, mutation_rate, fun_name):
    start = time.time()
    best_input, best_value, fitness_step, total_population_size= ga(population, mutation_rate, fun_name, 0)
    running_time = time.time() - start
    return best_input, best_value, fitness_step, total_population_size, running_time
