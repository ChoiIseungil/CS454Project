import math
from numpy import random
from GA import fitnesses, step
import time

def processing(generation, best_input, best_value, fun_name, k, fitness_step):
    fitnesses_results = []
    for population in generation:
        fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
        fitnesses_results.append(fitnesses_result)
    max_fitnesses_results = list(map(max ,fitnesses_results))
    sorted_index = sorted(range(len(max_fitnesses_results)), key=max_fitnesses_results.__getitem__)
    temp_value = max_fitnesses_results[sorted_index[-1]]
    if temp_value > best_value:
        best_index = sorted_index[-1]
        best_value = max_fitnesses_results[best_index]
        best_population = generation[best_index]
        best_fitnesses = fitnesses_results[best_index]
        best_index = best_fitnesses.index(max(best_fitnesses))
        best_input = best_population[best_index]
    if len(generation) > k:
        new_generation = []
        for i in range(k):
            new_generation.append(generation[sorted_index[-1 * (i+1)]])
        generation = new_generation
    return generation, fitnesses_results, best_input, best_value, fitness_step

def pga(population, mutation_rate, fun_name, n, m, k, fitness_step):
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
    generation = [population]
    fitnesses_results = [fitnesses_result]
    while generation_step < 10:
        new_generation = []
        for index, population in enumerate(generation):
            fitnesses_result = fitnesses_results[index]
            for i in range(n):
                new_population = step(population, fitnesses_result, population_size, fun_name, mutation_rate)
                new_generation.append(new_population)
            for i in range(m):
                generation_index = list(range(0, len(generation)))
                crossover_population_index = random.choice(generation_index)
                population_ = generation[crossover_population_index]
                fitnesses_result_, fitness_step = fitnesses(population_, best_value, fun_name, fitness_step)
                fitnesses_result += fitnesses_result_
                population = population + population_
                new_population = step(population, fitnesses_result, population_size, fun_name, mutation_rate)
                new_generation.append(new_population)
        generation, fitnesses_results, best_input, best_value, fitness_step = processing(new_generation, best_input, best_value, fun_name, k, fitness_step)
        total_population_size += len(generation) * population_size
        if total_population_size % 10 == 0:
            print('population size = {}, best_value = {}'.format(total_population_size, best_value))
        if best_value >= 1.0:
            return best_input, best_value, fitness_step, total_population_size
        generation_step += 1
    return best_input, best_value, fitness_step, total_population_size

def main(population, mutation_rate, fun_name, n, m, k):
    start = time.time()
    best_input, best_value, fitness_step, total_population_size = pga(population, mutation_rate, fun_name, n, m, k, 0)
    running_time = time.time() - start
    return best_input, best_value, fitness_step, total_population_size, running_time