import random
import logging
from genomes.bit_vector_genome import BitVectorGenome


class SurprisingSequencesProblem(object):
    def __init__(self,
                 vector_length,
                 fitness_function,
                 adult_selection_function,
                 parent_selection_function,
                 pheno_from_geno_function,
                 population_size,
                 n_reproducing_couples,
                 crossover_chance,
                 mutation_chance,
                 alphabet_size):
        self.fitness_function = fitness_function
        self.adult_selection_function = adult_selection_function
        self.parent_selection_function = parent_selection_function
        self.pheno_from_geno_function =\
            pheno_from_geno_function

        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.vector_length = vector_length
        self.population_size = population_size
        self.n_reproducing_couples = n_reproducing_couples
        self.alphabet_size = alphabet_size

    def generate_initial_genotypes(self):
        return [BitVectorGenome(vector_length=self.vector_length,
                                alphabet_size=self.alphabet_size,
                                randomize=True)
                for child in range(self.population_size)]

    def generate_phenotypes_from_genotypes(self,
                                           genotypes):
        return self.pheno_from_geno_function(genotypes)

    def test_children_and_select_adults(self,
                                        children,
                                        adults):
        children_fitness_scores = self._calculate_fitness_scores(children)
        adults_fitness_scores = self._calculate_fitness_scores(adults)

        children_with_fitness = zip(children, children_fitness_scores)
        adults_with_fitness = zip(adults, adults_fitness_scores)

        logging.info("Fitness in:\nChildren %s\nAdults %s",
                     children_with_fitness,
                     adults_with_fitness)

        new_adults = self.adult_selection_function(children_with_fitness,
                                                   adults_with_fitness,
                                                   self.population_size)

        logging.info("Fitness scores out: %s",
                     zip(new_adults,
                         self._calculate_fitness_scores(new_adults)))

        return new_adults

    def _calculate_fitness_scores(self,
                                  phenotypes):
        fitness_scores = [
            self.fitness_function(phenotype)
            for phenotype in phenotypes
            ]

        return fitness_scores

    def select_parents(self,
                       adults):
        adults_fitness = self._calculate_fitness_scores(adults)

        parents =\
            self.parent_selection_function(adults,
                                           adults_fitness,
                                           self.n_reproducing_couples)

        return parents

    def reproduce(self, parents):
        offspring_genotypes = []

        for mother, father in parents:
            if random.random() > self.crossover_chance:
                offspring_genotypes\
                    .append(BitVectorGenome(bit_vector_genome=mother))

                offspring_genotypes\
                    .append(BitVectorGenome(bit_vector_genome=father))
            else:
                for i in range(2):
                    crossover_point = random.randrange(self.vector_length)

                    offspring = BitVectorGenome(
                        value_vector=
                        mother.value_vector[:crossover_point] +
                        father.value_vector[crossover_point:])

                    offspring_genotypes.append(offspring)

        for offspring_genotype in offspring_genotypes:
            for i in range(len(offspring_genotype.value_vector)):
                if random.random() < self.mutation_chance:
                    offspring_genotype.value_vector[i] =\
                        random.randint(0, self.alphabet_size)

        return offspring_genotypes,\
            self._calculate_fitness_scores(offspring_genotypes)

    def get_winner(self, genotypes):
        win_fitness = 1.0
        for genotype in genotypes:
            if self.fitness_function(genotype) == win_fitness:
                return genotype

        return None
