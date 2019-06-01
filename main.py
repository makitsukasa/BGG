import datetime
import numpy as np
import warnings
from bgg import BGG
from RestrictedPopulation import RestrictedPopulation
from RestrictedElites import RestrictedElites
from problem.frontier.sphere      import sphere
from problem.frontier.ktablet     import ktablet
from problem.frontier.bohachevsky import bohachevsky
from problem.frontier.ackley      import ackley
from problem.frontier.schaffer    import schaffer
from problem.frontier.rastrigin   import rastrigin

warnings.simplefilter("error", RuntimeWarning)

def save(system, result, method_name, problem_name, index):
	if method_name in best_fitnesses:
		best_fitnesses[method_name].append(system.get_best_fitness())
	else:
		best_fitnesses[method_name] = [system.get_best_fitness()]
	if SAVE_HISTORY_CSV:
		filename = "benchmark/評価値_{0}_{1}_{2}.csv"\
			.format(method_name, problem_name, index)
		with open(filename, "w") as f:
			for c, v in system.history.items():
				f.write("{0},{1}\n".format(c, v))
			f.close()
	if SAVE_DISTANCE_CSV:
		filename = "benchmark/距離_{0}_{1}_{2}.csv"\
			.format(method_name, problem_name, index)
		with open(filename, "w") as f:
			for c, v in system.mean_of_distance_history.items():
				f.write("{0},{1}\n".format(c, v))
			f.close()

SAVE_HISTORY_CSV = False
SAVE_DISTANCE_CSV = False
SAVE_COUNTS_CSV = True

N = 20

PROBLEMS = [
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * N, "nchi" : 6 * N},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" : 10 * N, "nchi" : 6 * N},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  8 * N, "nchi" : 6 * N},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  8 * N, "nchi" : 6 * N},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 11 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 24 * N, "nchi" : 8 * N},
]

for problem in PROBLEMS:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	npar = N + 1
	nchi = problem["nchi"]
	best_fitnesses = {}
	# max_eval_count = 4000
	max_eval_count = 1000
	loop_count = 100

	print(name, loop_count, flush = True)

	for i in range(loop_count):
		method_name = "JGG"
		bgg = BGG(N, npop, npar, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_partitioned
		bgg.barometer = lambda: 1
		result = bgg.until(1e-7, max_eval_count)
		save(bgg, result, method_name, name, i)

		method_name = "序盤は集団がランダムな3n(t=1e-2)"
		ep = RestrictedPopulation(N, 3 * N, npar, 2 * N, npop, npar, nchi, func)
		ep.should_expand = ep.is_stucked
		ep.t = 1e-2
		result = ep.until(1e-7, max_eval_count)
		save(ep, result, method_name, name, i)

		method_name = "序盤は集団がランダムな5n(t=1e-2)"
		ep = RestrictedPopulation(N, 5 * N, npar, 2 * N, npop, npar, nchi, func)
		ep.should_expand = ep.is_stucked
		ep.t = 1e-2
		result = ep.until(1e-7, max_eval_count)
		save(ep, result, method_name, name, i)

	for method_name, best_fitness in best_fitnesses.items():
		print(
			method_name,
			np.average(best_fitness),
			sep = ","
		)

		if SAVE_COUNTS_CSV:
			filename = "benchmark2/検定_{0}_{1}.csv".format(name, method_name)
			with open(filename, "w") as f:
				for c in best_fitness:
					f.write("{}\n".format(c))
				f.close()
