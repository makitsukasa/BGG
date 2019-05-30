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
	if result:
		if method_name in eval_counts:
			eval_counts[method_name].append(system.eval_count)
		else:
			eval_counts[method_name] = [system.eval_count]
	else:
		print(method_name, "failed")
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

SAVE_HISTORY_CSV = True
SAVE_DISTANCE_CSV = True
SAVE_COUNTS_CSV = False

n = 20

problems = [
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * n, "nchi" : 6 * n},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" : 10 * n, "nchi" : 6 * n},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  8 * n, "nchi" : 6 * n},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  8 * n, "nchi" : 6 * n},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 11 * n, "nchi" : 8 * n},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 24 * n, "nchi" : 8 * n},
]

datestr = "{0:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())

for problem in problems:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	npar = n + 1
	nchi = problem["nchi"]
	eval_counts = {}
	max_eval_count = 4000
	loop_count = 10

	print(name, loop_count, flush = True)

	for i in range(loop_count):
		method_name = "JGG"
		bgg = BGG(n, npop, npar, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_partitioned
		bgg.barometer = lambda: 1
		result = bgg.until(1e-7, max_eval_count)
		save(bgg, result, method_name, name, i)

		method_name = "序盤は集団がランダムな3n(t=1e-2)"
		ep = RestrictedPopulation(n, 3 * n, npar, 2 * n, npop, npar, nchi, func)
		ep.should_expand = ep.is_stucked
		ep.t = 1e-2
		result = ep.until(1e-7, max_eval_count)
		save(ep, result, method_name, name, i)

		method_name = "序盤は集団がランダムな5n(t=1e-2)"
		ep = RestrictedPopulation(n, 5 * n, npar, 2 * n, npop, npar, nchi, func)
		ep.should_expand = ep.is_stucked
		ep.t = 1e-2
		result = ep.until(1e-7, max_eval_count)
		save(ep, result, method_name, name, i)

	for method_name, best_fitness in eval_counts.items():
		print(
			method_name,
			np.average(best_fitness),
			loop_count - len(best_fitness),
			sep = ","
		)

		if SAVE_COUNTS_CSV:
			filename = "benchmark/検定_{0}_{1}.csv".format(name, method_name)
			with open(filename, "w") as f:
				for c in best_fitness:
					f.write("{}\n".format(c))
				f.close()
