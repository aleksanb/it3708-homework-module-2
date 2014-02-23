import random


def fitness_proportionate(adults,
                          adults_fitness,
                          n_reproducing_couples):
    adults_with_fitness_dict = dict(zip(adults, adults_fitness))
    sum_fitness = float(sum(adults_fitness))

    parents = []

    for i in range(n_reproducing_couples):
        mother = _roulette_wheel(sum_fitness, adults_with_fitness_dict)
        father = _roulette_wheel(sum_fitness, adults_with_fitness_dict)
        parents.append((mother, father))

    return parents


def _roulette_wheel(sum_fitness,
                    adults_with_fitness_dict):
    fraction = random.uniform(0, sum_fitness)
    accu = 0

    for adult, fitness in adults_with_fitness_dict.items():
        accu += fitness
        if accu >= fraction:
            return adult


def uniform_selection(adults,
                      adults_fitness,
                      n_reproducing_couples):

    uniform_fitness = [1 for i in range(len(adults))]
    return fitness_proportionate(adults,
                                 uniform_fitness,
                                 n_reproducing_couples)


def sigma_scaling(adults,
                  adults_fitness,
                  n_reproducing_couples):
    vector_length = float(len(adults_fitness))
    fitness_average = sum(adults_fitness) / vector_length
    fitness_variance = sum([
                           (fitness_score - fitness_average)**2
                           for fitness_score in adults_fitness
                           ]) / vector_length

    fitness_std = fitness_variance ** 0.5

    sigma_fitness_scores = map(lambda fitness:
                               1 + ((fitness - fitness_average)
                                    / 2*fitness_std),
                               adults_fitness)

    return fitness_proportionate(adults,
                                 sigma_fitness_scores,
                                 n_reproducing_couples)


def tournament_selection_factory(epsilon, tournament_size):
    def tournament_selection(adults,
                             adults_fitness,
                             n_reproducing_couples):
        adults_with_fitness = zip(adults, adults_fitness)

        parents = []

        for couple in range(n_reproducing_couples):
            mother = _tourney(adults_with_fitness, tournament_size, epsilon)
            father = _tourney(adults_with_fitness, tournament_size, epsilon)
            parents.append((mother, father))

        return parents

    return tournament_selection


def _tourney(adults_with_fitness, tournament_size, epsilon):
    tournament_group = random.sample(adults_with_fitness, tournament_size)
    tournament_group.sort(key=lambda arr: arr[1],
                          reverse=True)

    if random.random() > epsilon:
        winner = tournament_group[0]
    else:
        winner = tournament_group[1:][random.randrange(tournament_size - 1)]

    return winner[0]
