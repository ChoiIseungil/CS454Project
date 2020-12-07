import csv
import random

f = open('hanoi_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        population.append(random.randint(1,10000))
    populations.append(population)

wr.writerow(populations)