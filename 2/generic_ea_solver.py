import logging


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
        # logging.info("*** Genotypes ***\n%s\n*** Genotypes ***\n",
        #              genotypes)

        #logging.info("#Generation Max Avg Std")

        while generation < self.generation_limit and not winner:
            generation += 1
            #logging.info("\n\n\n*** Generation %i ***", generation)

            children =\
                self.ea_problem.generate_phenotypes_from_genotypes(genotypes)

            # logging.info("Generated %i children. \n%s\n",
            #              len(children),
            #              children)

            adults =\
                self.ea_problem.test_children_and_select_adults(children,
                                                                adults)
            # logging.info("But only %i children grew up: \n%s\n",
            #              len(adults),
            #              adults)

            parents = self.ea_problem.select_parents(adults)

            # logging.info("And the %i lucky parents are: \n%s\n",
            #              len(parents),
            #              parents)

            genotypes, fitness_scores = self.ea_problem.reproduce(parents)

            gen_avg = sum(fitness_scores) / float(len(fitness_scores))
            gen_var = sum([(fitness - gen_avg) ** 2
                          for fitness in fitness_scores])\
                / float(len(fitness_scores))
            gen_std = gen_var ** 0.5

            # logging.info("%s %s %s %s",
            #              generation,
            #              max(fitness_scores),
            #              gen_avg,
            #              gen_std)

            # logging.info("We have %i beautiful genotypes: \n%s\n",
            #              len(genotypes),
            #              genotypes)

            winner = self.ea_problem.get_winner(genotypes)

        return generation, winner
