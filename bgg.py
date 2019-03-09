import numpy as np
from individual import Individual

class BGG:
	def __init__(self, n, npop, npar, nchi, problem):
		self.n = n
		self.npar = npar
		self.nchi = nchi
		self.eval_count = 0
		self.problem = problem
		self.population = [Individual(self.n) for i in range(npop)]
		for i in self.population:
			i.fitness = self.problem(i.gene)
		self.history = {}
		self.history[0] = np.average([i.fitness for i in self.population])
		# self.history[0] = np.amin([i.fitness for i in self.population])

	def barometer(self):
		l = len(self.history)
		if l > 10:
			return 1.0
		return l / 10

	def selection_for_reproduction(self):
		self.population.sort(key = lambda i: i.fitness)
		best = self.population[0].fitness
		worst = self.population[-1].fitness
		b = self.barometer()
		self.population.sort(key = lambda i:
			b * (best + np.random.rand() * (worst - best)) + (1.0 - b) * i.fitness)
		parents = self.population[:self.npar]
		self.population = self.population[self.npar:]
		return parents

	def crossover(self, parents):
		mu = len(parents)
		mean = np.mean(np.array([parent.gene for parent in parents]), axis = 0)
		children = [Individual(self.n) for i in range(self.nchi)]
		for child in children:
			epsilon = np.random.uniform(-np.sqrt(3 / mu), np.sqrt(3 / mu), mu)
			child.gene = mean + np.sum(
				[epsilon[i] * (parents[i].gene - mean) for i in range(mu)], axis = 0)
		return children

	def selection_for_survival(self, parents, children):
		children.sort(key = lambda i: i.fitness)
		return children[:self.npar]

	def evaluate(self, pop):
		for individual in pop:
			individual.fitness = self.problem(individual.gene)
		self.eval_count += len(pop)
		self.history[self.eval_count] = np.average([i.fitness for i in pop])
		return pop

	def alternation(self):
		parents = self.selection_for_reproduction()
		children = self.crossover(parents)
		self.evaluate(children)
		elites = self.selection_for_survival(parents, children)
		self.population.extend(elites)

	def until(self, goal, max_alt_count):
		for _ in range(max_alt_count):
			self.alternation()
			if self.get_best_fitness() < goal:
				return True
		return False

	def get_best_fitness(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness

if __name__ == '__main__':
	n = 20
	ga = BGG(n, 6 * n, n + 1, 6 * n, lambda x: np.sum((x * 10.24 - 5.12) ** 2))

	for i in range(230):
		ga.alternation()
	# print(ga.get_best_evaluation_value())

	for c, v in ga.history.items():
		print(c, v)
