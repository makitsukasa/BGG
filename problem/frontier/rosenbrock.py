import numpy as np

# R_star in https://www.jstage.jst.go.jp/article/tjsai/24/1/24_1_147/_article/-char/ja/
def rosenbrock(x):
	shifted = x * 4.096 - 2.048
	f = shifted[1:]
	return np.sum(100 * np.power(shifted[0] - np.power(f, 2.0), 2.0) + np.power(1.0 - f, 2.0))
