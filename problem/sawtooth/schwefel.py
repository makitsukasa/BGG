import numpy as np

def schwefel(x):
	shifted = x * 1000 - 500
	return np.sum(418.9829 - shifted * np.sin(np.sqrt(abs(shifted))))
