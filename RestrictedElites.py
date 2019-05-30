import datetime
import plot
import numpy as np
from individual import Individual

class RestrictedElites:
	def __init__(
			self,
			n,
			npop_restricted,
			npar_restricted,
			nchi_restricted,
			deadline,
			npop,
			npar,
			nchi,
			problem):
		self.n = n
		self.npop = npop_restricted
		self.npar = npar_restricted
		self.nchi = nchi_restricted
		self.deadline = deadline
		self.npop_full = npop
		self.npar_full = npar
		self.nchi_full = nchi
		self.problem = problem
		self.eval_count = 0
		self.expanded = False
		population = [Individual(n) for i in range(npop)]
		for i in population:
			i.fitness = self.problem(i.gene)
		population.sort(key = lambda x: x.fitness)
		self.population_nonelites = population[npop_restricted:]
		self.population = population[:npop_restricted]
		self.history = {0 : self.get_best_fitness()}
		self.mean_of_distance_history = {}

	def calc_mean_of_distance(self, parents):
		sum_ = 0
		l = len(parents)
		for i in range(l):
			for j in range(i + 1, l):
				i_th_array = np.array(parents[i].gene)
				j_th_array = np.array(parents[j].gene)
				sum_ += np.linalg.norm(i_th_array - j_th_array)
		return sum_ / (l * (l - 1) / 2)

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
		if not self.expanded and self.eval_count > self.deadline:
			self.expanded = True
			npop_restricted = self.npop
			self.npop = self.npop_full
			self.npar = self.npar_full
			self.nchi = self.nchi_full
			self.population.extend(self.population_nonelites)

	def until(self, goal, max_eval_count):
		while self.eval_count < max_eval_count:
			self.alternation()
			if self.get_best_fitness() < goal:
				return True
		return False

	def get_best_fitness(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness
