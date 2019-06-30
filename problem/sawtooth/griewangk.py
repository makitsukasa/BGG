import numpy as np

def griewangk(x):
	shifted = x * 100 - 50
	hoge = np.sum(shifted ** 2) / 4000
	piyo = np.prod(np.cos([shifted[i] / np.sqrt(i + 1) for i in range(len(x))]))
	return hoge - piyo + 1
