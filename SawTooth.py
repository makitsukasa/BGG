import numpy as np
from individual import Individual

class SawTooth:
	def __init__(
			self,
			n,
			npop_mean,
			npop_range,
			npar,
			nchi,
			tooth_width,
			problem):
		self.n = n
		self.npop_mean = npop_mean
		self.npop_range = npop_range
		self.tooth_width = tooth_width
		self.npop = npop_mean + npop_range
		self.npar = npar
		self.nchi = nchi
		self.problem = problem
		self.eval_count = 0
		self.generation_count = 0
		self.population = [Individual(self.n) for i in range(self.npop)]
		for i in self.population:
			i.fitness = self.problem(i.gene)
		self.history = {0 : self.get_best_fitness()}
		self.avg_history = {0: np.average([i.fitness for i in self.population])}

	def get_next_pop_size(self):
		t = self.generation_count + 1
		return int(self.npop_mean + self.npop_range - 2 * self.npop_range *\
			(t - 1 - self.tooth_width * int((t - 1) / self.tooth_width)) / (self.tooth_width - 1))

	def adjust_pop_size(self):
		delta_pop_size = self.get_next_pop_size() - len(self.population)
		# print(len(self.population), "->", self.get_next_pop_size(), ", delta:", delta_pop_size)
		if delta_pop_size < 0:
			self.population.sort(key = lambda i: i.fitness if i.fitness else np.Infinity)
			self.population = self.population[:delta_pop_size]
		else:
			new_comer = [Individual(self.n) for i in range(delta_pop_size)]
			for i in new_comer:
				i.fitness = self.problem(i.gene)
			self.population.extend(new_comer)

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
			ng = True
			while ng:
				epsilon = np.random.uniform(-np.sqrt(3 / mu), np.sqrt(3 / mu), mu)
				child.gene = mean + np.sum(
					[epsilon[i] * (parents[i].gene - mean) for i in range(mu)], axis = 0)
				ng = False
				for g in child.gene:
					if g < 0.0 or g > 1.0:
						ng = True
						break
			# print("gene", child.gene)
		return children

	def select_for_survival(self, parents, children):
		family = children[:]
		family.extend(parents)
		family.sort(key = lambda i: i.fitness)
		return family[:self.npar]

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
		# self.mean_of_distance_history[self.eval_count] =\
		# 	self.calc_mean_of_distance(parents)
		self.adjust_pop_size()
		# print(self.generation_count, self.eval_count, len(self.population), self.get_best_fitness())
		self.generation_count += 1

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

