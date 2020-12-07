import csv
import random

f = open('gcd_population.csv', 'w')
wr = csv.writer(f)

populations = []
for i in range(10):
    population = []
    for j in range(5):
        coins = []
        total_num = 0
        for k in range(random.randint(1, 100)):
            coin = random.randint(1, 100)
            coins.append(coin)
            total_num += coin
        total = random.randint(1, total_num)
        gene = [coins, total]
        population.append(gene)
    populations.append(population)

wr.writerow(populations)