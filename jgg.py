import numpy as np
from individual import Individual

class JGG:
	def __init__(self, n, problem):
		self.n = n
		self.problem = problem

	def initialize(self, npop):
		self.population = [Individual(self.n) for i in range(npop)]
		return self.population

	def reproduction(self, npar):
		np.random.shuffle(self.population)
		self.parents = self.population[:npar]
		return self.parents

	def crossover(self, nchi):
		mu = len(self.parents)
		mean = np.mean(np.array([parent.gene for parent in self.parents]), axis = 0)
		self.children = [Individual(self.n) for i in range(nchi)]
		for child in self.children:
			epsilon = np.random.normal(0.0, np.sqrt(1 / (mu - 1)), mu)
			child.gene = mean + np.sum(
				[epsilon[i] * (self.parents[i].gene - mean) for i in range(mu)], axis = 0)
		return self.children

	def survival_selection(self, npar):
		self.evaluate(self.children)
		self.children.sort(key = lambda child: child.fitness)
		self.population[:npar] = self.children[:npar]
		return self.population

	def evaluate(self, pop):
		for s in pop:
			s.fitness = self.problem(s.gene)

	def get_best_evaluation_value(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness, self.population[0].gene

if __name__ == '__main__':
	n = 5
	ga = JGG(n, lambda x: np.sum(x**2))

	ga.initialize(14 * n)
	for i in range(300):
		ga.reproduction(n + 1)
		ga.crossover(5 * n)
		ga.survival_selection(n + 1)
	print(ga.get_best_evaluation_value())
