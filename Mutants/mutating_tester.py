import os
from importlib import import_module

def get_mutants(name):
    mutants = []
    for file in os.listdir("Mutants/" + name):
        if file.startswith(name):
            mutants.append(getattr(import_module("{}.{}".format("Mutants." + name, file.split('.')[0])), name))
    return mutants

def calc_mutation_score(mutants, inputs):
    ans_list = []
    for input in inputs:
        try:
            ans_list.append(mutants[0](*input))
        except Exception as e:
            ans_list.append(e)

    mut_num = 0
    mut_kill = 0
    mut_surv = 0
    for mutant in mutants[1:]:
        for ans, input in zip(ans_list, inputs):
            try:
                if mutant(*input) != ans:
                    mut_kill += 1
                    break
            except Exception as e:
                if e != ans:
                    mut_kill += 1
                    break
        else:
            mut_surv += 1
        mut_num += 1

    return mut_kill / mut_num

def get_mutation_score(name, inputs):
    return calc_mutation_score(get_mutants(name), inputs)

# if __name__ == "__main__":
#     print(get_mutation_score('hanoi', [[17, 1, 3], [7, 1, 3]]))