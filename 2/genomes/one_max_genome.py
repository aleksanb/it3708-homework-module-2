class OneMaxGenome:
    def __init__(self, vector_length=0, init_value=0, value_vector=None):
    	if (value_vector == None):
        	self.value_vector = [init_value for iter in range(vector_length)]
        else:
        	self.value_vector = value_vector

    def __repr__(self):
    	return str(self.value_vector)