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
            pga = True
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

    if pga:
        best_input, best_value, fitness_step, running_time = PGA.main(population, mutation_rate, fun_name, n, m, k)
    else:
        best_input, best_value, fitness_step, running_time = GA.main(population, mutation_rate, fun_name)
    print(best_input, best_value, fitness_step, running_time)

if __name__ == '__main__':
    main()