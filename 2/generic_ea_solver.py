from problems.one_max_problem import OneMaxProblem
from fitness_functions import one_max_fitness
import logging
import multiprocessing


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

            children = self.ea_problem.generate_phenotypes_from_genotypes(
                genotypes
            )

            logging.info("Generated %i children.", len(children))

            adults = self.ea_problem.test_children_and_select_adults(children,
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


##########################
# Begin setup            #
##########################

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
    one_max_problem = OneMaxProblem(vector_length=VECTOR_LENGTH,
                                    fitness_function=one_max_fitness,
                                    population_size=POPULATION_SIZE,
                                    n_reproducing_couples=
                                    N_REPRODUCING_COUPLES,
                                    crossover_chance=CROSSOVER_CHANCE,
                                    mutation_chance=MUTATION_CHANCE)

    return GenericEaSolver(one_max_problem,
                           GENERATION_LIMIT).start_simulation()

##########################
# Initializing variables #
##########################

POPULATION_SIZE = 100
N_REPRODUCING_COUPLES = POPULATION_SIZE / 2
VECTOR_LENGTH = 40
GENERATION_LIMIT = 10000

CROSSOVER_CHANCE = 0.9
MUTATION_CHANCE = 0.01

N_RUNS = 100

#############################
# Be nice, say hi to people #
#############################

print_with_wrap("Welcome to Generic EA Solver Version 1337")
print_variables()
#logging.basicConfig(level=logging.INFO)

###########################
# Creating CPU threadpool #
###########################

cpus = multiprocessing.cpu_count() - 1
print "{0} computational cores available, ".format(cpus) +\
    "redirecting all power to EA-1337\n"
pool = multiprocessing.Pool(processes=cpus)

while True:
    default_or_exit = raw_input("Customize defaults? (y/n/q)")
    if default_or_exit == "y":
        N_RUNS = set_or_default("Number of runs", N_RUNS)
        POPULATION_SIZE = set_or_default("Children pool size",
                                         POPULATION_SIZE)
        N_REPRODUCING_COUPLES = set_or_default("Number of reproducing couples",
                                               N_REPRODUCING_COUPLES)
        VECTOR_LENGTH = set_or_default("Bit vector length", VECTOR_LENGTH)
        GENERATION_LIMIT = set_or_default("Generation limit", GENERATION_LIMIT)
        CROSSOVER_CHANCE = set_or_default("Crosover rate", CROSSOVER_CHANCE)
        MUTATION_CHANCE = set_or_default("Mutation rate", MUTATION_CHANCE)
    elif default_or_exit == "q":
        break

    print_with_wrap("Starting simulation ({} runs)".format(N_RUNS))

    term_gens = pool.map(omx_factory, xrange(N_RUNS))

    #for i in range(N_RUNS):
        #term_gens.append(omx_factory(i))
        #print "Finished with run {}".format(i)

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