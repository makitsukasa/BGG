import datetime
import numpy as np
import warnings
from bgg import BGG
from NeighborFirst import NeighborFirst
from problem.frontier.sphere      import sphere
from problem.frontier.ktablet     import ktablet
from problem.frontier.bohachevsky import bohachevsky
from problem.frontier.ackley      import ackley
from problem.frontier.schaffer    import schaffer
from problem.frontier.rastrigin   import rastrigin

warnings.simplefilter("error", RuntimeWarning)

SAVE_HISTORY_CSV = False
SAVE_DISTANCE_CSV = False
SAVE_COUNTS_CSV = True

n = 20

problems = [
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * n, "nchi" : 6 * n},
	{"name" : "k-tablet",    "func" : ktablet,     "npop" : 10 * n, "nchi" : 6 * n},
	{"name" : "bohachevsky", "func" : bohachevsky, "npop" :  8 * n, "nchi" : 6 * n},
	{"name" : "ackley",      "func" : ackley,      "npop" :  8 * n, "nchi" : 6 * n},
	{"name" : "schaffer",    "func" : schaffer,    "npop" : 11 * n, "nchi" : 8 * n},
	{"name" : "rastrigin",   "func" : rastrigin,   "npop" : 24 * n, "nchi" : 8 * n},
]

datestr = "{0:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())

for problem in problems:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	nchi = problem["nchi"]
	best_fitnesses = {}
	max_eval_count = 60 * n
	loop_count = 100

	print(name, loop_count, flush = True)

	for i in range(loop_count):
		method_name = "JGG"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_partitioned
		bgg.barometer = lambda: 1
		result = bgg.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(bgg.get_best_fitness())
		else:
			best_fitnesses[method_name] = [bgg.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in bgg.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "親の50％は最良個体の近傍"
		nf = NeighborFirst(n, npop, n + 1, nchi, func)
		nf.select_for_reproduction =\
			lambda : nf.select_for_reproduction_partitioned(0.5, 1200)
		# nf.calc_mean_of_distance = lambda hoge: 0
		result = nf.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(nf.get_best_fitness())
		else:
			best_fitnesses[method_name] = [nf.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "親の60％は最良個体の近傍"
		nf = NeighborFirst(n, npop, n + 1, nchi, func)
		nf.select_for_reproduction =\
			lambda : nf.select_for_reproduction_partitioned(0.6, 1200)
		# nf.calc_mean_of_distance = lambda hoge: 0
		result = nf.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(nf.get_best_fitness())
		else:
			best_fitnesses[method_name] = [nf.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "親の70％は最良個体の近傍"
		nf = NeighborFirst(n, npop, n + 1, nchi, func)
		nf.select_for_reproduction =\
			lambda : nf.select_for_reproduction_partitioned(0.7, 1200)
		# nf.calc_mean_of_distance = lambda hoge: 0
		result = nf.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(nf.get_best_fitness())
		else:
			best_fitnesses[method_name] = [nf.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "親の80％は最良個体の近傍"
		nf = NeighborFirst(n, npop, n + 1, nchi, func)
		nf.select_for_reproduction =\
			lambda : nf.select_for_reproduction_partitioned(0.8, 1200)
		# nf.calc_mean_of_distance = lambda hoge: 0
		result = nf.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(nf.get_best_fitness())
		else:
			best_fitnesses[method_name] = [nf.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "親の90％は最良個体の近傍"
		nf = NeighborFirst(n, npop, n + 1, nchi, func)
		nf.select_for_reproduction =\
			lambda : nf.select_for_reproduction_partitioned(0.9, 1200)
		# nf.calc_mean_of_distance = lambda hoge: 0
		result = nf.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(nf.get_best_fitness())
		else:
			best_fitnesses[method_name] = [nf.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "親の100％は最良個体の近傍"
		nf = NeighborFirst(n, npop, n + 1, nchi, func)
		nf.select_for_reproduction =\
			lambda : nf.select_for_reproduction_partitioned(1.0, 1200)
		# nf.calc_mean_of_distance = lambda hoge: 0
		result = nf.until(1e-7, max_eval_count)
		if method_name in best_fitnesses:
			best_fitnesses[method_name].append(nf.get_best_fitness())
		else:
			best_fitnesses[method_name] = [nf.get_best_fitness()]
		if SAVE_HISTORY_CSV:
			filename = "benchmark/序盤_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()
		if SAVE_DISTANCE_CSV:
			filename = "benchmark/距離_{0}_{1}.csv"\
				.format(method_name, name)
			with open(filename, "w") as f:
				for c, v in nf.mean_of_distance_history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

	for method_name, best_fitness in best_fitnesses.items():
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
