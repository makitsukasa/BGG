import numpy as np

def rastrigin(x):
	shifted = x * 10 - 5
	return sum([(i**2 + 10 - 10 * np.cos(2 * np.pi * i)) for i in shifted])
