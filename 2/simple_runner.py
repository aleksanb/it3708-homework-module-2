import logging
from problems import *
import multiprocessing
import generic_ea_solver

import fitness_functions
import adult_selection_functions
import parent_selection_functions
import pheno_from_geno_functions


def print_with_wrap(wrapee):
    print "___________________________________________________\n"
    print "    {0}    ".format(wrapee)
    print "___________________________________________________\n"

# Constants

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

ALPHABET_SIZE = 10
GENERATION_LIMIT = 400

POPULATION_SIZE = 50
N_REPRODUCING_COUPLES = POPULATION_SIZE * 3 / 4

CROSSOVER_CHANCE = 0.9
MUTATION_CHANCE = 0.01

#logging.basicConfig(level=logging.INFO)

# CPU stuff
N_RUNS = 1  # multiprocessing.cpu_count()
NO_MERCY = True

cpus = multiprocessing.cpu_count()
print "{0} computational cores available, ".format(cpus) +\
    "redirecting {0} cores to EA-1337\n".format(cpus - 1 + NO_MERCY)

pool = multiprocessing.Pool(processes=cpus - 1 + NO_MERCY)

print "Number of runs:      ", N_RUNS, "\n", \
    "\nAlphabet             ", ALPHABET_SIZE, "\n", \
    "\nPopulation size:     ", POPULATION_SIZE, \
    "\nRepr. couples:       ", N_REPRODUCING_COUPLES, \
    "\nGeneration limit:    ", GENERATION_LIMIT,\
    "\nCrossover chance:    ", CROSSOVER_CHANCE,\
    "\nMutation chance:     ", MUTATION_CHANCE, "\n"


def ea_with_param(vector_length):
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

    return generation, winner

print_with_wrap("Running with alphabet size {0}. Checking length from 0 to {1}"
                .format(ALPHABET_SIZE, ALPHABET_SIZE * 3))
results = []
for vector_length in range(1, ALPHABET_SIZE * 3):
    generation, winner = ea_with_param(vector_length)

    results.append((generation, winner))
    print "Returned from {0}".format(vector_length),\
        "with timeout" if generation == GENERATION_LIMIT\
        else "with winner {0}".format(winner),\
        "at generation {0}".format(generation)
