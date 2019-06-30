import numpy as np

def rosenbrock(x):
	shifted = x * 2.0
	ans = 0
	for i in range(len(x) - 1):
		ans += 100 * (shifted[i + 1] - shifted[i] ** 2) ** 2 + (1 - shifted[i]) ** 2
	return ans
