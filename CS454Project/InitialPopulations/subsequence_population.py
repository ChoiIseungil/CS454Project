import csv
import random

f = open('gcd_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        a = random.randint(1, 100)
        b = random.randint(a, a + 100)
        k = random.randint(1, b - a + 1)
        gene = [a, b, k]
        population.append(gene)
    populations.append(population)

wr.writerow(populations)