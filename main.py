import sys
import getopt
import csv
import GA
import PGA
import random
from tester import Tester


def main():
    pga = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],'p:m:n:l:c:r:')
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(1)

    pga = "False"
    mutation_rate = 0.05
    arg_num = 5
    max_value = 20
    condition_range = 5
    error_rate = 0.3

    for opt, arg in opts:
        if (opt == '-p'):
            pga = arg
        elif (opt == '-m'):
            mutation_rate = float(arg)
        elif (opt == '-n'):
            arg_num = int(arg)
        elif (opt == '-l'):
            max_value = int(arg)
        elif (opt == '-c'):
            condition_range = int(arg)
        elif (opt == '-r'):
            error_rate = float(arg)


    population = []
    for _ in range(10):
        sequence = []
        for _ in range(5):
            gene = []
            for _ in range(arg_num):
                gene.append(random.randint(0,max_value))
            sequence.append(gene)
        population.append(sequence)
    
    evaluator = Tester()
    # evaluator.reset(argnum=arg_num, max_value=max_value, condition_range=condition_range, error_rate=error_rate, correction_range=[])
    evaluator.reset(argnum=arg_num, max_value=max_value, condition_range=condition_range, error_rate=error_rate, correction_range = [[(0, range(0,3), 0.7), (1, range(0,3), 0.7), (2, range(0,3), 0.7)] ,[(0, range(3,6), 0.7), (1, range(3,6), 0.7), (2, range(3,6), 0.7)] ,[(0, range(6,9), 0.7), (1, range(6,9), 0.7), (2, range(6,9), 0.7)]])

    if pga == "True":
        best_input, best_value, fitness_step, total_population_size, running_time = PGA.main(population = population, mutation_rate = mutation_rate, evaluator = evaluator, n = 3, m = 1, k = 20) # n, m, k hyperparamter
    else:
        best_input, best_value, fitness_step, total_population_size, running_time = GA.main(population = population, mutation_rate = mutation_rate, evaluator = evaluator)
    print(best_value, fitness_step, total_population_size, running_time)

if __name__ == '__main__':
    main()