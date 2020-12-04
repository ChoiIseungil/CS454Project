import csv
import random

f = open('hanoi_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        population.append([random.randint(1,500),random.randint(10,200)]) #epsilon = 0.001~0.2
    populations.append(population)

wr.writerow(populations)