import random
from genomes.one_max_genome import OneMaxGenome

class OneMaxProblem:
    fitness_function = None

    win_condition = None
    vector_length = 0

    children_pool_size = 0
    adult_pool_size = 0


    def __init__(self, win_condition, vector_length, fitness_function, children_pool_size, adult_pool_size): # Initialize child genotype population
        self.fitness_function = fitness_function

        self.win_condition = win_condition
        self.vector_length = vector_length

        self.children_pool_size = children_pool_size
        self.adult_pool_size = adult_pool_size

    def generate_initial_genotypes(self):
        return [OneMaxGenome(vector_length=self.vector_length) for child in range(self.children_pool_size)]
    
    def generate_phenotypes_from_genotypes(self, genotypes):
        return genotypes

    def test_phenotype_fitness(self, children):
        return [self.fitness_function(child) for child in children]

    def select_adults(self, adults, children, children_fitness_scores):
        """A-I: Full Generational Replacement

            Kill all adults, all children survive

        """
        return children


        """A-II: Over-production

            Select n children from m available where n < m

        """
        #return random.sample(children, self.adult_pool_size)

        """A-III: Generational Mixing

            Coming soon (tm)

        """

    def select_parents(self, adults):
        sum_fitness = float(sum([self.fitness_function(adult) for adult in adults]))
        choices = {adult:self.fitness_function(adult) for adult in adults}

        parents = []

        for i in range(self.children_pool_size / 2):
            mother = self._roulette_wheel(sum_fitness, choices)
            father = self._roulette_wheel(sum_fitness, choices)
            parents.append((mother, father))

        return parents

    def _roulette_wheel(self, sum_fitness, choices):
        fraction = random.uniform(0, sum_fitness)
        accu = 0

        for adult, fitness in choices.items():
            accu += fitness
            if accu > fraction: # We have a winRAR!
                return adult


    def reproduce(self, parents):
        offspring_genotypes = []

        for mother, father in parents:
            #print "Mother: ", mother, "\nFather: ", father

            # Single point crossover
            for i in range(2):
                crossover_point = random.randrange(self.vector_length)

                offspring = OneMaxGenome(
                    value_vector=
                        mother.value_vector[:crossover_point] +
                        father.value_vector[crossover_point:])
                offspring_genotypes.append(offspring)

                #print "Child: " , offspring, " (split at ", crossover_point, " )"

            #print "\n"


        for offspring_genotype in offspring_genotypes:
            #print "Pre-mutate: ", offspring_genotype.value_vector
            flip_point = random.randrange(self.vector_length)
            offspring_genotype.value_vector[flip_point] = 1 - offspring_genotype.value_vector[flip_point]
            #print "Post-mutate: ", offspring_genotype.value_vector

        return offspring_genotypes

    def get_winner(self, genotypes):
        print "Best fitness new generation: ", max([self.fitness_function(genotype) for genotype in genotypes])
        for genotype in genotypes:
            if (self.vector_length + 1) == self.fitness_function(genotype):
                return True

        return False
