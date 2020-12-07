import math
from numpy import random
from GA import fitnesses, step

def processing(generation, best_input, best_value, fun_name, k, fitness_step):
    fitnesses_results = []
    for population in generation:
        fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
        fitnesses_results.append(fitnesses_result)
    fitnesses_results = list(map(best ,fitnesses_results))
    sorted_index = sorted(range(len(fitnesses_results)), key=lambda k: fitnesses_results[k]).reverse()
    temp_value = fitnesses_results[sorted_index[0]]
    if temp_value > best_value:
        best_index = sorted_index[0]
        best_value = fitnesses_results[best_index]
        best_population = generation[best_index]
        best_fitnesses = fitnesses_results[best_index]
        best_index = best_fitnesses.index(max(best_fitnesses))
        best_input = best_population[best_index]
    if len(generation) > k:
        new_generation = []
        for i in range(k):
            new_generation.append(generation[sorted_index[i]])
        generation = new_generation
    return generation, best_input, best_value

def pga(population, mutation_rate, fun_name, n, m, k, fitness_step):
    step = 0
    best_value = 0
    population_size = len(population)
    fitnesses_result, fitness_step = fitnesses(population, best_value, fun_name, fitness_step)
    best_index = fitnesses_result.index(max(fitnesses_result))
    best_value = fitnesses_result[best_index]
    best_input = population[best_index]
    if best_value >= 100:
        return best_input, best_value, fitness_step
    generation = [population]
    while step < 25:
        new_generation = []
        for population in generation:
            for i in range(n):
                new_population = step(population, fitnesses_result, population_size, mutation_rate)
                new_generation.append(new_population)
            for i in range(m):
                population_ = random.choice(generation)
                population = population + population_
                new_population = step(population, fitnesses_result, population_size, mutation_rate)
                new_generation.append(new_population)
        generation, best_input, best_value, fitness_step = processing(new_generation, best_input, best_value, fun_name, k, fitness_step)
        if best_value >= 100:
            return best_input, best_value, fitness_step 
        step += 1
    return best_input, best_value, fitness_step

def main(population, mutation_rate, fun_name, n, m, k):
    start = time.time()
    best_input, best_value, fitness_step = pga(population, mutation_rate, fun_name, n, m, k, 0)
    running_time = time.time() - start
    return best_input, best_value, fitness_step, running_time