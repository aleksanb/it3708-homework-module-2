def omf_reward(one_max_genome):
    return sum(one_max_genome.value_vector)


def omf_punish(one_max_genome):
    error = len(one_max_genome.value_vector)\
        - sum(one_max_genome.value_vector)

    return 1 / float(1 + error)
