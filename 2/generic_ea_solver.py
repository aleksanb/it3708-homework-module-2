from problems.one_max_problem import OneMaxProblem
from fitness_functions import one_max_fitness

class GenericEaSolver:
    ea_problem = None

    def __init__(self, ea_problem):
        self.ea_problem = ea_problem

    def start_simulation(self):
        # Init variables
        genotypes = []
        children = []
        adults = []
        winner = None
        generation = 0

        # Init values
        genotypes = self.ea_problem.generate_initial_genotypes()
        print "*** Genotypes ***\n", genotypes, "\n*** Genotypes ***\n"

        while not winner:
            generation += 1
            print "\n*** Generation ", generation, " ***"

            children = self.ea_problem.generate_phenotypes_from_genotypes(genotypes)
            #print "Phenotypes generated for ", len(children), " Phenotypes"

            children_fitness_scores = self.ea_problem.test_phenotype_fitness(children)
            #print len(children_fitness_scores), " children have the following fitness scores: ", children_fitness_scores
            #print "Best score of this generation: ", max(children_fitness_scores)

            adults = self.ea_problem.select_adults(adults, children, children_fitness_scores)
            #print "But only ", len(adults), " of the children got to grow up to become adults :("

            parents = self.ea_problem.select_parents(adults)
            #print "The lucky parents are: ", parents

            genotypes = self.ea_problem.reproduce(parents)
            #print "And the beautiful children are: ", children

            winner = self.ea_problem.get_winner(genotypes);

        print "Found winRAR ", winner

WIN_CONDITION = 20
VECTOR_LENGTH = 10
CHILDREN_POOL_SIZE = 10
ADULT_POOL_SIZE = 8

one_max_problem = OneMaxProblem(WIN_CONDITION, VECTOR_LENGTH, one_max_fitness, CHILDREN_POOL_SIZE, ADULT_POOL_SIZE)

GenericEaSolver(one_max_problem).start_simulation()
