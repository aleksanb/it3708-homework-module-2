import logging
from itertools import repeat
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

FITNESS_FUNCTION = fitness_functions\
    .surprising_punish
    #.surprising_local_punish

ADULT_SELECTION_FUNCTION =\
    adult_selection_functions.full_generational_replacement

PARENT_SELECTION_FUNCTION =\
    parent_selection_functions\
    .tournament_selection_factory(tournament_size=8, epsilon=0.1)

GENERATION_LIMIT = 1000

POPULATION_SIZE = 150
N_REPRODUCING_COUPLES = POPULATION_SIZE / 2

CROSSOVER_CHANCE = 0.9
MUTATION_CHANCE = 0.01

N_RUNS = 1  # multiprocessing.cpu_count()
NO_MERCY = True

print "Number of runs:      ", N_RUNS, "\n", \
    "\nAlphabet             ", 1337, "\n", \
    "\nPopulation size:     ", POPULATION_SIZE, \
    "\nRepr. couples:       ", N_REPRODUCING_COUPLES, \
    "\nGeneration limit:    ", GENERATION_LIMIT,\
    "\nCrossover chance:    ", CROSSOVER_CHANCE,\
    "\nMutation chance:     ", MUTATION_CHANCE, "\n"


def ea_with_param((alphabet_size, vector_length)):
    print "Alph: ", alphabet_size, "length, ", vector_length
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
                     alphabet_size=alphabet_size - 1)

    generation, winner = generic_ea_solver\
        .GenericEaSolver(omp,
                         GENERATION_LIMIT).start_simulation()

    print "Alph: ", alphabet_size, "length, ", vector_length, "terminating."

    return generation, vector_length, winner


def solve_for_alphabet_size(alphabet_size, pool):
    print "Alph: ", alphabet_size, " starting execution!"
    solutions = pool.map(ea_with_param,
                         zip(repeat(alphabet_size),
                             range(1, alphabet_size * 3 + 1)))

    #for v_length in range(1, ALPHABET_SIZE * 3 + 1):
        # print "Alph:", alphabet_size, "starting length:", v_length
        # generation, winner = ea_with_param(alphabet_size, v_length)
        # solutions[v_length] = (generation, winner)
        # print "Alph:", alphabet_size, "found solution for length",\
        #     v_length, winner

    return solutions


#logging.basicConfig(level=logging.INFO)

# CPU stuff
cpus = multiprocessing.cpu_count()
print "{0} computational cores available, ".format(cpus) +\
    "redirecting {0} cores to EA-1337\n".format(cpus - 1 + NO_MERCY)
pool = multiprocessing.Pool(processes=cpus - 1 + NO_MERCY)

all_solutions = {}
for alphabet_size in range(3, 21):
    print "Alph: ", alphabet_size, " starting execution!"
    solutions = pool.map(ea_with_param,
                         zip(repeat(alphabet_size),
                             range(1, alphabet_size * 3 + 1)))

    print "Solutions for", alphabet_size, "for lengths up to ",\
        alphabet_size * 3, solutions, "\n"
    all_solutions[alphabet_size] = solutions

print "All solutions:"
print all_solutions
