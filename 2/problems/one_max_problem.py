import random
import logging
from genomes.bit_vector_genome import BitVectorGenome


class OneMaxProblem:
    #highest_found_fitness = 0

    def __init__(self,
                 vector_length,
                 fitness_function,
                 population_size,
                 n_reproducing_couples,
                 crossover_chance,
                 mutation_chance):
        self.fitness_function = fitness_function
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance

        self.vector_length = vector_length

        self.population_size = population_size
        self.n_reproducing_couples = n_reproducing_couples

    def generate_initial_genotypes(self):
        return [
            BitVectorGenome(vector_length=self.vector_length,
                            randomize=True)
            for child in range(self.population_size)
            ]

    def generate_phenotypes_from_genotypes(self,
                                           genotypes):
        return genotypes

    def test_children_and_select_adults(self,
                                        children,
                                        adults):

        children_fitness_scores = self._calculate_fitness_scores(children)
        adults_fitness_scores = self._calculate_fitness_scores(adults)

        #logging.info("Fitness scores in:\nChildren: %s\nParents %s",
                     #children_fitness_scores,
                     #adults_fitness_scores)

        #if max(children_fitness_scores) > self.highest_found_fitness:
            #self.highest_found_fitness = max(children_fitness_scores)
            #print self.highest_found_fitness

        #return children

        new_adults = self.\
            _select_adults(children,
                           children_fitness_scores,
                           adults,
                           adults_fitness_scores)

        logging.info("Fitness scores out: %s",
                     self._calculate_fitness_scores(new_adults))

        return new_adults

    def _calculate_fitness_scores(self,
                                  phenotypes):
        fitness_scores = [
            self.fitness_function(phenotype)
            for phenotype in phenotypes
            ]

        # fitness_average = sum(fitness_scores) / self.vector_length
        # fitness_variance = sum([
        #     (fitness_score - fitness_average)**2
        #     for fitness_score in fitness_scores
        #     ]) / float(self.vector_length)

        return fitness_scores

    def _select_adults(self,
                       children,
                       children_fitness_scores,
                       adults,
                       adults_fitness_scores):

        gene_pool = children + adults
        fitness_pool = children_fitness_scores + adults_fitness_scores
        fitness_zipped_genes = zip(fitness_pool, gene_pool)
        fitness_zipped_genes.sort(key=lambda arr: arr[0],
                                  reverse=True)
        selected_adults = map(lambda arr: arr[1],
                              fitness_zipped_genes[:self.population_size])

        return selected_adults

    def select_parents(self,
                       adults):
        sum_fitness = float(sum([
            self.fitness_function(adult) for adult in adults]))

        choices = {
            adult: self.fitness_function(adult)
            for adult in adults
            }

        parents = []

        for i in range(self.n_reproducing_couples):
            mother = self._roulette_wheel(sum_fitness, choices)
            father = self._roulette_wheel(sum_fitness, choices)
            parents.append((mother, father))

        return parents

    def _roulette_wheel(self,
                        sum_fitness,
                        choices):
        fraction = random.uniform(0, sum_fitness)
        accu = 0

        for adult, fitness in choices.items():
            accu += fitness
            if accu >= fraction:
                return adult

    def reproduce(self, parents):
        offspring_genotypes = []

        for mother, father in parents:
            # Single point crossover
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
                if random.random() <= self.mutation_chance:
                    offspring_genotype.value_vector[i] =\
                        1 - offspring_genotype.value_vector[i]

        return offspring_genotypes

    def get_winner(self, genotypes):
        for genotype in genotypes:
            if (self.vector_length) == self.fitness_function(genotype):
                return genotype

        return None
