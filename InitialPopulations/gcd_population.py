import csv
import random

f = open('gcd_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        gene = [random.randint(0, 1000), random.randint(0, 1000)]
        population.append(gene)
    populations.append(population)

wr.writerow(populations)