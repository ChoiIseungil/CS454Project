import csv
import random

f = open('hanoi_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        capacity = random.randint(1,100)
        items = []
        for k in range(random.randint(1, 10)):
            weight = random.randint(1,capacity)
            value = random.randint(1,10)
            items.append([weight, value])
        gene = [capacity, items]
        population.append(gene)
    populations.append(population)

wr.writerow(populations)