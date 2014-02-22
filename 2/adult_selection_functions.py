

def full_generational_replacement(children_with_fitness,
                                  adults_with_fitness,
                                  population_size):
    selected_adults = map(lambda arr: arr[0], children_with_fitness)

    return selected_adults


def over_production(children_with_fitness,
                    adults_with_fitness,
                    population_size):
    children_with_fitness.sort(key=lambda arr: arr[1],
                               reverse=True)

    selected_adults = map(lambda arr: arr[0],
                          children_with_fitness[:population_size])

    return selected_adults


def generational_mixing(children_with_fitness,
                        adults_with_fitness,
                        population_size):
    fitness_pool = children_with_fitness + adults_with_fitness
    fitness_pool.sort(key=lambda arr: arr[1],
                      reverse=True)

    selected_adults = map(lambda arr: arr[0],
                          fitness_pool[:population_size])

    return selected_adults
