def omf_reward(one_max_genome):
    return sum(one_max_genome.value_vector)


def omf_punish(one_max_genome):
    error = len(one_max_genome.value_vector)\
        - sum(one_max_genome.value_vector)

    return 1 / float(1 + error)


def surprising_punish(genome):
    sequences = set()
    error = 0
    g = genome.value_vector

    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            t = (g[i], g[j], j - i)
            if t in sequences:
                error += 1
            else:
                sequences.add(t)

    return 1 / float(1 + error)


def surprising_local_punish(genome):
    sequences = set()
    error = 0
    g = genome.value_vector

    for i in range(len(g) - 1):
        t = (g[i], g[i + 1])
        if t in sequences:
            error += 1
        else:
            sequences.add(t)

    return 1 / float(1 + error)
