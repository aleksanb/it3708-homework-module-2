from problems.one_max_problem import OneMaxProblem
import logging
import multiprocessing

import fitness_functions
import adult_selection_functions
import parent_selection_functions


class GenericEaSolver:
    def __init__(self,
                 ea_problem,
                 generation_limit):

        self.ea_problem = ea_problem
        self.generation_limit = generation_limit

    def start_simulation(self):

        # Init variables
        genotypes = []
        children = []
        adults = []
        winner = None
        generation = 0

        # Init values
        genotypes = self.ea_problem.generate_initial_genotypes()
        logging.info("*** Genotypes ***\n%s\n*** Genotypes ***\n",
                     genotypes)

        while generation < self.generation_limit and not winner:
            generation += 1
            logging.info("\n*** Generation %i ***", generation)

            children =\
                self.ea_problem.generate_phenotypes_from_genotypes(genotypes)

            logging.info("Generated %i children.", len(children))

            adults =\
                self.ea_problem.test_children_and_select_adults(children,
                                                                adults)
            logging.info("But only %i children grew up", len(adults))

            parents = self.ea_problem.select_parents(adults)
            genotypes = self.ea_problem.reproduce(parents)
            winner = self.ea_problem.get_winner(genotypes)

        #print_with_wrap(
            #" Simulation terminated (Gen {0} of {1})".format(
                #generation,
                #self.generation_limit))

        #print "WinRAR? ", winner, winner.value_vector, "\n"
        return generation


############################
## Begin setup            ##
############################

def print_variables():
    print "Number of runs:      ", N_RUNS, "\n", \
        "\nPopulation size:     ", POPULATION_SIZE, \
        "\nRepr. couples:       ", N_REPRODUCING_COUPLES, \
        "\nVector length:       ", VECTOR_LENGTH, \
        "\nGeneration limit:    ", GENERATION_LIMIT,\
        "\nCrossover chance:    ", CROSSOVER_CHANCE,\
        "\nMutation chance:     ", MUTATION_CHANCE, "\n"


def print_with_wrap(wrapee):
    print "___________________________________________________\n"
    print "    {0}    ".format(wrapee)
    print "___________________________________________________\n"


def set_or_default(label, variable):
    inpt = raw_input(label + ":  (Default: " + str(variable) + ") ")
    return int(inpt) if inpt else variable


def omx_factory(i):
    print "I'm {0}".format(i)
    omp = OneMaxProblem(vector_length=VECTOR_LENGTH,
                        fitness_function=FITNESS_FUNCTION,
                        adult_selection_function=
                        ADULT_SELECTION_FUNCTION,
                        parent_selection_function=
                        PARENT_SELECTION_FUNCTION,
                        population_size=POPULATION_SIZE,
                        n_reproducing_couples=N_REPRODUCING_COUPLES,
                        crossover_chance=CROSSOVER_CHANCE,
                        mutation_chance=MUTATION_CHANCE)

    return GenericEaSolver(omp,
                           GENERATION_LIMIT).start_simulation()

############################
## Initializing variables ##
############################

FITNESS_FUNCTION =\
    fitness_functions\
    .omf_punish
    #.omf_reward

ADULT_SELECTION_FUNCTION =\
    adult_selection_functions\
    .full_generational_replacement
    #.over_production
    #.generational_mixing

PARENT_SELECTION_FUNCTION =\
    parent_selection_functions\
    .fitness_proportionate
    #.sigma_scaling
    #.tournament_selection_factory(tournament_size=20, epsilon=0.2)

#logging.basicConfig(level=logging.INFO)
N_RUNS = multiprocessing.cpu_count() * 4

POPULATION_SIZE = 200
N_REPRODUCING_COUPLES = POPULATION_SIZE / 2
VECTOR_LENGTH = 40
GENERATION_LIMIT = 400

CROSSOVER_CHANCE = 1.000
MUTATION_CHANCE = 0.001

NO_MERCY = True

###############################
## Be nice, say hi to people ##
###############################

print_with_wrap("Welcome to Generic EA Solver Version 1337")
print_variables()

#############################
## Creating CPU threadpool ##
#############################

cpus = multiprocessing.cpu_count()
print "{0} computational cores available, ".format(cpus) +\
    "redirecting {0} cores to EA-1337\n".format(cpus - 1 + NO_MERCY)

pool = multiprocessing.Pool(processes=cpus - 1 + NO_MERCY)

#############################
## Main loop               ##
#############################

while True:
    default_or_exit = raw_input("Customize defaults? (y/n/q)")
    if default_or_exit == "y":
        N_RUNS = set_or_default("Number of runs", N_RUNS)
        POPULATION_SIZE = set_or_default("Children pool size",
                                         POPULATION_SIZE)
        N_REPRODUCING_COUPLES = set_or_default("Reproducing couples",
                                               N_REPRODUCING_COUPLES)
        VECTOR_LENGTH = set_or_default("Bit vector length",
                                       VECTOR_LENGTH)
        GENERATION_LIMIT = set_or_default("Generation limit",
                                          GENERATION_LIMIT)
        CROSSOVER_CHANCE = set_or_default("Crosover rate",
                                          CROSSOVER_CHANCE)
        MUTATION_CHANCE = set_or_default("Mutation rate",
                                         MUTATION_CHANCE)
    elif default_or_exit == "q":
        break

    print_with_wrap("Starting simulation ({} runs)".format(N_RUNS))
    term_gens = pool.map(omx_factory, xrange(N_RUNS))

    avg_term_gen = sum(term_gens) / float(N_RUNS)
    term_gen_var = sum([(term_gen - avg_term_gen) ** 2
                       for term_gen in term_gens]) / float(N_RUNS)
    term_gen_std = term_gen_var ** 0.5

    print "\nTerminating generations:\n", term_gens,\
        "\nWith average: ", avg_term_gen,\
        "\nAnd standard deviaton: ", term_gen_std,\
        "\nMin: ", min(term_gens),\
        "\nMax: ", max(term_gens), "\n"

print_with_wrap("Thank you for using EA-1337")
