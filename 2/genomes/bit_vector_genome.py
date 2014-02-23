import random
from copy import deepcopy


class BitVectorGenome(object):
    def __init__(self,
                 vector_length=0,
                 alphabet_size=None,
                 value_vector=None,
                 randomize=False,
                 bit_vector_genome=None,
                 create_solution=False):
        if bit_vector_genome is not None:
            self.value_vector = deepcopy(bit_vector_genome.value_vector)
        elif value_vector is not None:
            self.value_vector = deepcopy(value_vector)
        elif alphabet_size is None:
            if create_solution is True:
                self.value_vector = [1 for iter in range(vector_length)]
            elif randomize is True:
                self.value_vector = [
                    random.randint(0, 1)
                    for iter in range(vector_length)]
            else:
                self.value_vector = [0 for iter in range(vector_length)]
        else:
            if randomize is True:
                self.value_vector = [
                    random.randint(0, alphabet_size - 1)
                    for iter in range(vector_length)]
            else:
                self.value_vector = [0 for iter in range(vector_length)]

    def __repr__(self):
        return str(self.value_vector)
