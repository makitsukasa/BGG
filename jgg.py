import numpy as np
from individual import Individual

# 用語は 遺伝的アルゴリズムにおける世代交代モデルの提案と評価(佐藤，97)による

class JGG:
	def __init__(self, n, npop, npar, nchi, problem):
		self.n = n
		self.npar = npar
		self.nchi = nchi
		self.problem = problem
		self.population = [Individual(self.n) for i in range(npop)]
		self.history = []
		self.history.append(np.average([self.problem(i.gene) for i in self.population]))
		# self.history.append(np.amin([self.problem(i.gene) for i in self.population]))

	def selection_for_reproduction(self):
		np.random.shuffle(self.population)
		parents = self.population[:self.npar]
		self.population = self.population[self.npar:]
		return parents

	def crossover(self, parents):
		mu = len(parents)
		mean = np.mean(np.array([parent.gene for parent in parents]), axis = 0)
		children = [Individual(self.n) for i in range(self.nchi)]
		for child in children:
			epsilon = np.random.normal(0.0, np.sqrt(1 / (mu - 1)), mu)
			child.gene = mean + np.sum(
				[epsilon[i] * (parents[i].gene - mean) for i in range(mu)], axis = 0)
		return children

	def selection_for_survival(self, children):
		children.sort(key = lambda child: child.fitness)
		return children[:self.npar]

	def evaluate(self, pop):
		for individual in pop:
			individual.fitness = self.problem(individual.gene)
		self.history.append(np.average([i.fitness for i in pop]))
		return pop

	def alternation(self):
		parents = self.selection_for_reproduction()
		children = self.crossover(parents)
		self.evaluate(children)
		elites = self.selection_for_survival(children)
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

	def get_eval_count(self):
		return len(self.history) * self.nchi

if __name__ == '__main__':
	n = 20
	ga = JGG(n, 6 * n, n + 1, 6 * n, lambda x: np.sum((x * 10.24 - 5.12) ** 2))

	for i in range(230):
		ga.alternation()
	print(ga.get_best_fitness())

	for h in ga.history:
		print(h)
