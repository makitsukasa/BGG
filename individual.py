import numpy as np

class Individual:
	def __init__(self, n):
		# initialized by random values
		if isinstance(n, int):
			self.n = n
			self.gene = np.random.uniform(0, 1, n)

		# initialized by list
		else:
			self.n = len(n)
			self.gene = n

		self.fitness = None

	def __str__(self):
		return "{f}:{g}".format(
			f = 'None' if self.fitness     is None else '{:.4}'.format(self.fitness),
			g = ','.join(['{:.4}'.format(g) for g in self.gene])
		)
