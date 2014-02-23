import logging
from problems import *
import multiprocessing
import generic_ea_solver

import fitness_functions
import adult_selection_functions
import parent_selection_functions
import pheno_from_geno_functions

############################
## Begin setup            ##
############################


def print_variables():
    print "# Number of runs:      ", N_RUNS, "\n", \
        "\n# Population size:     ", POPULATION_SIZE, \
        "\n# Repr. couples:       ", N_REPRODUCING_COUPLES, \
        "\n# Vector length:       ", VECTOR_LENGTH, \
        "\n# Generation limit:    ", GENERATION_LIMIT,\
        "\n# Crossover chance:    ", CROSSOVER_CHANCE,\
        "\n# Mutation chance:     ", MUTATION_CHANCE, "\n"


def print_with_wrap(wrapee):
    print "#_________________________________________________#\n#"
    print "#    {0}    ".format(wrapee)
    print "#_________________________________________________#\n"


def set_or_default(label, variable):
    inpt = raw_input(label + ":  (Default: " + str(variable) + ") ")
    return int(inpt) if inpt else variable


def ea_problem_factory(i):
    # print "Forking {0}".format(i)
    ea_problem = EA_PROBLEM(vector_length=VECTOR_LENGTH,
                            fitness_function=FITNESS_FUNCTION,
                            adult_selection_function=
                            ADULT_SELECTION_FUNCTION,
                            parent_selection_function=
                            PARENT_SELECTION_FUNCTION,
                            pheno_from_geno_function=
                            PHENO_FROM_GENO_FUNCTION,
                            population_size=POPULATION_SIZE,
                            n_reproducing_couples=N_REPRODUCING_COUPLES,
                            crossover_chance=CROSSOVER_CHANCE,
                            mutation_chance=MUTATION_CHANCE)

    generation, winner = generic_ea_solver\
        .GenericEaSolver(ea_problem,
                         GENERATION_LIMIT).start_simulation()
    print "Returned from {0}".format(i),\
        "with timeout" if generation == GENERATION_LIMIT\
        else "with winner {0}".format(winner),\
        "at generation {0}".format(generation)

    return generation, winner


def surprising_global_factory():
    print_with_wrap("Running with alphabet size {0}." +
                    "Checking length from 0 to {1}"
                    .format(ALPHABET_SIZE, ALPHABET_SIZE * 3))
    results = []
    for vector_length in range(0, ALPHABET_SIZE * 3):
        omp = EA_PROBLEM(vector_length=vector_length,
                         fitness_function=FITNESS_FUNCTION,
                         adult_selection_function=
                         ADULT_SELECTION_FUNCTION,
                         parent_selection_function=
                         PARENT_SELECTION_FUNCTION,
                         pheno_from_geno_function=
                         PHENO_FROM_GENO_FUNCTION,
                         population_size=POPULATION_SIZE,
                         n_reproducing_couples=N_REPRODUCING_COUPLES,
                         crossover_chance=CROSSOVER_CHANCE,
                         mutation_chance=MUTATION_CHANCE,
                         alphabet_size=ALPHABET_SIZE)

        generation, winner = generic_ea_solver\
            .GenericEaSolver(omp,
                             GENERATION_LIMIT).start_simulation()

        results.append((generation, winner))
        print "Returned from {0}".format(vector_length),\
            "with timeout" if generation == GENERATION_LIMIT\
            else "with winner {0}".format(winner),\
            "at generation {0}".format(generation)

############################
## Initializing variables ##
############################
"""
EA_PROBLEM =\
    surprising_sequences_problem.SurprisingSequencesProblem


PHENO_FROM_GENO_FUNCTION =\
    pheno_from_geno_functions.identity_function

FITNESS_FUNCTION =\
    fitness_functions.surprising_punish

ADULT_SELECTION_FUNCTION =\
    adult_selection_functions.full_generational_replacement

PARENT_SELECTION_FUNCTION =\
    parent_selection_functions\
    .tournament_selection_factory(tournament_size=8, epsilon=0.2)

"""
ALPHABET_SIZE = 10
"""
# VECTOR_LENGTH = 26
GENERATION_LIMIT = 400

POPULATION_SIZE = 10
N_REPRODUCING_COUPLES = POPULATION_SIZE / 2

CROSSOVER_CHANCE = 0.02
MUTATION_CHANCE = 0.01
"""
EA_PROBLEM =\
    one_max_problem.OneMaxProblem

PHENO_FROM_GENO_FUNCTION =\
    pheno_from_geno_functions.identity_function

FITNESS_FUNCTION =\
    fitness_functions\
    .omf_punish
    #.omf_reward

ADULT_SELECTION_FUNCTION =\
    adult_selection_functions\
    .full_generational_replacement
    #.generational_mixing
    #.over_production

PARENT_SELECTION_FUNCTION =\
    parent_selection_functions\
    .fitness_proportionate
    #.tournament_selection_factory(tournament_size=8, epsilon=0.2)
    #.sigma_scaling"""

POPULATION_SIZE = 80
N_REPRODUCING_COUPLES = POPULATION_SIZE / 2  # / 2
VECTOR_LENGTH = 40
GENERATION_LIMIT = 400

CROSSOVER_CHANCE = 1
MUTATION_CHANCE = 0.01

log_file = "results/omx-{0}-{1}-{2}".format(POPULATION_SIZE,
                                            CROSSOVER_CHANCE,
                                            MUTATION_CHANCE)

logging.basicConfig(level=logging.INFO,
                    format='%(message)s',
                    filename=log_file)
N_RUNS = 1  # multiprocessing.cpu_count() * 10
NO_MERCY = True

#############################
## Creating CPU threadpool ##
#############################

cpus = multiprocessing.cpu_count()
print "{0} computational cores available, ".format(cpus) +\
    "redirecting {0} cores to EA-1337\n".format(cpus - 1 + NO_MERCY)

pool = multiprocessing.Pool(processes=cpus - 1 + NO_MERCY)

###############################
## Be nice, say hi to people ##
###############################

#print_with_wrap("Welcome to Generic EA Solver Version 1337")
print_variables()

#############################
## Main loop               ##
#############################

while True:
    #############################
    ## Take input from user    ##
    #############################

    # default_or_exit = raw_input("Customize defaults? (y/n/q)")
    # if default_or_exit == "y":
    #     N_RUNS = set_or_default("Number of runs", N_RUNS)
    #     POPULATION_SIZE = set_or_default("Children pool size",
    #                                      POPULATION_SIZE)
    #     N_REPRODUCING_COUPLES = set_or_default("Reproducing couples",
    #                                            N_REPRODUCING_COUPLES)
    #     # VECTOR_LENGTH = set_or_default("Bit vector length",
    #     #                                VECTOR_LENGTH)
    #     GENERATION_LIMIT = set_or_default("Generation limit",
    #                                       GENERATION_LIMIT)
    #     CROSSOVER_CHANCE = set_or_default("Crosover rate",
    #                                       CROSSOVER_CHANCE)
    #     MUTATION_CHANCE = set_or_default("Mutation rate",
    #                                      MUTATION_CHANCE)
    # elif default_or_exit == "q":
    #     break

    print_with_wrap("Starting simulation ({} runs)".format(N_RUNS))
    term_gens = pool.map(ea_problem_factory, xrange(N_RUNS))

    term_gens = map(lambda e: e[0], term_gens)
    #surprising_global_factory()

    #############################
    ## Post-calculation stats  ##
    #############################

    avg_term_gen = sum(term_gens) / float(N_RUNS)
    term_gen_var = sum([(term_gen - avg_term_gen) ** 2
                       for term_gen in term_gens]) / float(N_RUNS)
    term_gen_std = term_gen_var ** 0.5

    print "\nTerminating generations:\n", term_gens,\
        "\nWith average: ", avg_term_gen,\
        "\nAnd standard deviaton: ", term_gen_std,\
        "\nMin: ", min(term_gens),\
        "\nMax: ", max(term_gens), "\n"

    break

print_with_wrap("Thank you for using EA-1337")
