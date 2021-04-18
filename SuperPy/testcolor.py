import numpy as np
from numpy.random import default_rng
rng = default_rng(1234)



import os
print("PYTHONPATH:", os.environ.get('PYTHONPATH'))
print("PATH:", os.environ.get('PATH'))


integersA = rng.integers(low=0, high=500, size=216)
integersB = rng.integers(low=0, high=500, size=216)
integersMatrix = integersA * integersB
reshaped = np.reshape(integersMatrix, (6,6,6))
print(rng)
