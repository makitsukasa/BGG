import math
import datetime
import plot
import numpy as np
from individual import Individual

class NeighborFirst:
	def __init__(self, n, npop, npar, nchi, problem):
		self.n = n
		self.npar = npar
		self.npop = npop
		self.nchi = nchi
		self.eval_count = 0
		self.problem = problem
		self.population = [Individual(self.n) for i in range(npop)]
		for i in self.population:
			i.fitness = self.problem(i.gene)
		self.history = {0 : self.get_best_fitness()}
		self.mean_of_distance_history = {}

	@staticmethod
	def calc_distance(one, another):
		ones_array = np.array(one.gene)
		anothers_array = np.array(another.gene)
		return np.linalg.norm(ones_array - anothers_array)

	def calc_mean_of_distance(self, parents):
		sum_ = 0
		l = len(parents)
		for i in range(l):
			for j in range(i + 1, l):
				sum_ += NeighborFirst.calc_distance(parents[i], parents[j])
		return sum_ / (l * (l - 1) / 2)

	def crossover(self, parents):
		mu = len(parents)
		mean = np.mean(np.array([parent.gene for parent in parents]), axis = 0)
		children = [Individual(self.n) for i in range(self.nchi)]
		for child in children:
			epsilon = np.random.uniform(-np.sqrt(3 / mu), np.sqrt(3 / mu), mu)
			child.gene = mean + np.sum(
				[epsilon[i] * (parents[i].gene - mean) for i in range(mu)], axis = 0)
		return children

	def select_for_survival(self, parents, children):
		children.sort(key = lambda i: i.fitness)
		return children[:self.npar]

	def evaluate(self, pop):
		for individual in pop:
			individual.fitness = self.problem(individual.gene)
		self.eval_count += len(pop)
		return pop

	def alternation(self):
		parents = self.select_for_reproduction()
		children = self.crossover(parents)
		self.evaluate(children)
		elites = self.select_for_survival(parents, children)
		self.population.extend(elites)
		self.history[self.eval_count] = self.get_best_fitness()
		self.mean_of_distance_history[self.eval_count] =\
			self.calc_mean_of_distance(parents)

	def until(self, goal, max_eval_count):
		while self.eval_count < max_eval_count:
			self.alternation()
			if self.get_best_fitness() < goal:
				return True
		return False

	def get_best_fitness(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness

	def select_for_reproduction_jgg():
		np.random.shuffle(self.population)
		ret = self.population[:self.npar]
		self.population = self.population[self.npar:]
		return ret

	def select_for_reproduction_partitioned(self, neighborRatio, deadline):
		if self.eval_count > deadline:
			select_for_reproduction_jgg()
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		best = self.population[0]
		for i in self.population:
			i.neighboringness = NeighborFirst.calc_distance(best, i)
		nneighbor = math.floor(self.npar * neighborRatio)
		nbest = self.npar - nneighbor
		self.population.sort(key = lambda s: s.neighboringness)
		ret = self.population[:nneighbor]
		not_neighbor = self.population[nneighbor:]
		not_neighbor.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		ret.extend(not_neighbor[:nbest])
		return ret

	def select_for_reproduction_product(self, deadline):
		if self.eval_count > deadline:
			select_for_reproduction_jgg()
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		best = self.population[0]
		for i in self.population:
			neighboringness = NeighborFirst.calc_distance(best, i)
			i.product = i.fitness * neighboringness
		self.population.sort(key = lambda s: s.product)
		return self.population[:npar]

if __name__ == '__main__':
	n = 20
	ga = BGG(n, 6 * n, n + 1, 6 * n, lambda x: np.sum((x * 10.24 - 5.12) ** 2))
	ga.get_nchi = ga.get_nchi_fixed
	ga.select_for_reproduction = ga.select_for_reproduction_restricted
	ga.barometer = ga.barometer_linear(1200, 0)

	while ga.eval_count < 30000:
		ga.alternation()
	print(ga.get_best_fitness(), ga.eval_count)

	filename = "benchmark/{0:%Y-%m-%d_%H-%M-%S}.csv".format(datetime.datetime.now())
	with open(filename, "w") as f:
		for c, v in ga.history.items():
			f.write("{0},{1}\n".format(c, v))
		f.close()

	plot.plot(filename)
