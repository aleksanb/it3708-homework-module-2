

def full_generational_replacement(children,
                                  children_fitness_scores,
                                  adults,
                                  adults_fitness_scores,
                                  population_size):
    return children


def over_production(children,
                    children_fitness_scores,
                    adults,
                    adults_fitness_scores,
                    population_size):

    fitness_zipped_genes = zip(children, children_fitness_scores)
    fitness_zipped_genes.sort(key=lambda arr: arr[0],
                              reverse=True)

    selected_adults = map(lambda arr: arr[1],
                          fitness_zipped_genes[:population_size])

    return selected_adults


def generational_mixing(children,
                        children_fitness_scores,
                        adults,
                        adults_fitness_scores,
                        population_size):
    gene_pool = children + adults
    fitness_pool = children_fitness_scores + adults_fitness_scores
    fitness_zipped_genes = zip(fitness_pool, gene_pool)
    fitness_zipped_genes.sort(key=lambda arr: arr[0],
                              reverse=True)
    selected_adults = map(lambda arr: arr[1],
                          fitness_zipped_genes[:population_size])

    return selected_adults
