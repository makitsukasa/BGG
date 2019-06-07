import numpy as np
import plot
from individual import Individual

class PopulationSizeAdjusting:
	def __init__(
			self,
			n,
			adjust_opt,
			problem):
		self.n = n
		npop_first, npar_first, nchi_first, self.adjust_trigger = adjust_opt[0]
		self.npop = max(npop_first, npar_first)
		self.npar = npar_first
		self.nchi = nchi_first
		self.adjust_opt = adjust_opt
		self.problem = problem
		self.eval_count = 0
		self.adjust_count = 0
		self.population = [Individual(self.n) for i in range(self.npop)]
		self.stashed_population = []
		for i in self.population:
			i.fitness = self.problem(i.gene)
		self.history = {0 : self.get_best_fitness()}
		self.mean_of_distance_history = {}
		self.avg_history = {0: np.average([i.fitness for i in self.population])}

	def calc_mean_of_distance(self, parents):
		# return 0 ######################################################################
		sum_ = 0
		l = len(parents)
		for i in range(l):
			for j in range(i + 1, l):
				i_th_array = np.array(parents[i].gene)
				j_th_array = np.array(parents[j].gene)
				sum_ += np.linalg.norm(i_th_array - j_th_array)
		return sum_ / (l * (l - 1) / 2)

	def adjust_pop_size(self):
		self.adjust_count += 1
		npop_old = self.npop
		self.npop, self.npar, self.nchi, self.adjust_trigger =\
			self.adjust_opt[self.adjust_count]
		if npop_old > self.npop:
			np.random.shuffle(self.population)
			self.stashed_population.extend(self.population[self.npop:])
			self.population = self.population[:self.npop]
		else:
			required = self.npop - npop_old
			stashed = len(self.stashed_population)
			if stashed > required:
				self.population.extend(
					self.stashed_population[:required])
				self.stashed_population = self.stashed_population[required:]
			else:
				self.population.extend(self.stashed_population[:])
				self.stashed_population = []
				self.population.extend(
					[Individual(self.n) for _ in range(required - stashed)])
				for i in self.population:
					i.fitness = self.problem(i.gene)

	def select_for_reproduction(self):
		np.random.shuffle(self.population)
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

	def select_for_survival(self, _parents, children):
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
		self.avg_history[self.eval_count] =\
			np.average([i.fitness for i in self.population])
		self.mean_of_distance_history[self.eval_count] =\
			self.calc_mean_of_distance(parents)
		if eval(self.adjust_trigger):
			self.adjust_pop_size()

	def until(self, goal, max_eval_count):
		while self.eval_count < max_eval_count:
			self.alternation()
			if self.get_best_fitness() < goal:
				return True
		return False

	def get_best_fitness(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness

	def is_stucked(self, t):
		if len(self.avg_history) < 3:
			return False

		keys = [*self.avg_history.keys()]
		keys.sort()

		init_fitness = self.avg_history[0]
		most_recent_fitness = self.avg_history[keys[-1]]
		second_recent_fitness = self.avg_history[keys[-2]]

		diff_init_rec = init_fitness - most_recent_fitness
		diff_rec_rec = second_recent_fitness - most_recent_fitness
		if diff_init_rec != 0 and abs(diff_rec_rec / diff_init_rec) >= t:
			return False

		return True

	def is_over_deadline(self, deadline):
		return self.eval_count > deadline
