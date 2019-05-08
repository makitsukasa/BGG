import datetime
import plot
import numpy as np
from individual import Individual

class RestrictedPopulation:
	def __init__(self, n, npop_restricted, deadline, npop_full, npar, nchi, problem):
		self.n = n
		self.npar = npar
		self.npop_restricted = npop_restricted
		self.npop_full = npop_full
		self.nchi = nchi
		self.eval_count = 0
		self.problem = problem
		self.deadline = deadline
		self.expanded = False
		self.population = [Individual(self.n) for i in range(npop_restricted)]
		for i in self.population:
			i.fitness = self.problem(i.gene)
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
			self.population.extend(
				[Individual(self.n) for _ in range(self.npop_full - self.npop_restricted)])

	def until(self, goal, max_eval_count):
		while self.eval_count < max_eval_count:
			self.alternation()
			if self.get_best_fitness() < goal:
				return True
		return False

	def get_best_fitness(self):
		self.population.sort(key = lambda s: s.fitness if s.fitness else np.inf)
		return self.population[0].fitness
