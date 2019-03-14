import datetime
import plot
import numpy as np
from individual import Individual

class BGG:
	def __init__(self, n, npop, npar, nchi, problem):
		self.n = n
		self.npar = npar
		self.max_nchi = nchi
		self.eval_count = 0
		self.problem = problem
		self.population = [Individual(self.n) for i in range(npop)]
		for i in self.population:
			i.fitness = self.problem(i.gene)
		self.history = {}
		self.history[0] = self.get_best_fitness()

	def barometer(self):
		return min(self.eval_count / 1200, 1.0)

	def crossover(self, parents):
		mu = len(parents)
		mean = np.mean(np.array([parent.gene for parent in parents]), axis = 0)
		children = [Individual(self.n) for i in range(self.get_nchi())]
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
		return pop

	def alternation(self):
		parents = self.selection_for_reproduction()
		children = self.crossover(parents)
		self.evaluate(children)
		elites = self.selection_for_survival(parents, children)
		self.population.extend(elites)
		self.history[self.eval_count] = self.get_best_fitness()

	def until(self, goal, max_eval_count):
		while self.eval_count < max_eval_count:
			self.alternation()
			if self.get_best_fitness() < goal:
				return True
		return False

	def get_best_fitness(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness

	def get_nchi_fixed(self):
		return self.max_nchi

	def get_nchi_barotmetic(self):
		return max(int(self.barometer() * self.max_nchi), 2 * self.npar)

	def selection_for_reproduction_sloped_rand(self):
		self.population.sort(key = lambda i: i.fitness)
		best = self.population[0].fitness
		worst = self.population[-1].fitness
		b = self.barometer()
		self.population.sort(key = lambda i:
			b * (best + np.random.rand() * (worst - best)) + (1.0 - b) * i.fitness)
		parents = self.population[:self.npar]
		self.population = self.population[self.npar:]
		return parents

	def selection_for_reproduction_partitioned(self):
		random_num = min(int(self.npar * self.barometer()), self.npar)
		elite_num = self.npar - random_num
		self.population.sort(key = lambda i: i.fitness)
		elites = self.population[:elite_num]
		self.population = self.population[elite_num:]
		np.random.shuffle(self.population)
		randoms = self.population[:random_num]
		self.population = self.population[random_num:]
		ans = randoms
		ans.extend(elites)
		return ans

if __name__ == '__main__':
	n = 20
	ga = BGG(n, 6 * n, n + 1, 6 * n, lambda x: np.sum((x * 10.24 - 5.12) ** 2))
	ga.get_nchi = ga.get_nchi_fixed
	ga.selection_for_reproduction = ga.selection_for_reproduction_partitioned

	while ga.eval_count < 30000:
		ga.alternation()

	filename = "benchmark/{0:%Y-%m-%d_%H-%M-%S}.csv".format(datetime.datetime.now())
	with open(filename, "w") as f:
		for c, v in ga.history.items():
			f.write("{0},{1}\n".format(c, v))
		f.close()

	plot.plot(filename)
