import csv
import random

f = open('hanoi_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        height = random.randint(0,20)
        start = random.randint(1,3)
        end = random.randint(1,3)
        while end==start:
            end = random.randint(1,3)
        gene = [height,start,end]
        population.append(gene)
    populations.append(population)

wr.writerow(populations)