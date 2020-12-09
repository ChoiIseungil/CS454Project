import csv
import random

f = open('quicksort_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        items = []
        for k in range(random.randint(1, 100)):
            value = random.randint(1,100)
            items.append(value)
        gene = [items]
        population.append(gene)
    populations.append(population)

wr.writerow(populations)