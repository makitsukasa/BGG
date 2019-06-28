import numpy as np

# original Goldberg & Richardson function is max f. Optimum f = 1.0.
# Here, min f' := 1 - f.
def goldberg_richardson(x):
	f = 1
	for x_i in x:
		g = np.sin(5.1 * np.pi * x_i + 0.5)
		h = np.exp(-4.0 * np.log(2.0) * ((x_i - 0.0667) ** 2) / 0.64)
		f *= g * h
	return 1 - f
