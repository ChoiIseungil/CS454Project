import sys
import getopt
import csv
import GA
import PGA


def main():
    pga = False

    try:
        opts, args = getopt.getopt(sys.argv[1:],'p:m:f:')
    except getopt.GetoptError as err:
        print(str(err))
        help()
        sys.exit(1)

    for opt, arg in opts:
        if (opt == '-p'):
            pga = arg
        elif (opt == '-m'):
            mutation_rate = float(arg)
        elif (opt == '-f'):
            fun_name = arg

    f = open('./InitialPopulations/' + fun_name + '_population.csv', 'r')
    rdr = csv.reader(f)
    for line in rdr:
        population = line
    new_population = []
    for parameter in population:
        new_population.append(eval(parameter))
    population = new_population

    if pga == "True":
        best_input, best_value, fitness_step, total_population_size, running_time = PGA.main(population, mutation_rate, fun_name, 2, 1, 30) # n, m, k hyperparamter
    else:
        best_input, best_value, fitness_step, total_population_size, running_time = GA.main(population, mutation_rate, fun_name)
    print(best_value, fitness_step, total_population_size, running_time)

if __name__ == '__main__':
    main()