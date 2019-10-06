import warnings
import numpy as np
from PopulationSizeAdjusting import PopulationSizeAdjusting
from SawTooth import SawTooth
from problem.frontier.sphere      import sphere
from problem.frontier.ktablet     import ktablet
from problem.frontier.bohachevsky import bohachevsky
# from problem.frontier.ackley      import ackley
from problem.frontier.schaffer    import schaffer
# from problem.frontier.rastrigin   import rastrigin
from problem.sawtooth.schwefel  import schwefel
from problem.sawtooth.rastrigin import rastrigin
from problem.sawtooth.ackley    import ackley
from problem.sawtooth.griewangk import griewangk

warnings.simplefilter("error", RuntimeWarning)

def save(system, result, method_name, problem_name, index):
	if method_name in best_fitnesses:
		best_fitnesses[method_name].append(system.get_best_fitness())
	else:
		best_fitnesses[method_name] = [system.get_best_fitness()]
	if result:
		if method_name in eval_counts:
			eval_counts[method_name].append(system.eval_count)
		else:
			eval_counts[method_name] = [system.eval_count]
	else:
		print(method_name, "failed")
	# print(system.population[0].gene)

	if SAVE_HISTORY_CSV:
		filename = "benchmark/{0}_{1}_{2}.csv"\
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
SAVE_EVAL_COUNTS_CSV = True
SAVE_BEST_FITNESSES_CSV = False

N = 20

PROBLEMS = [
	# n = 10, goal = 1e-7
	# {"name" : "sphere",      "func" : sphere,      "npop" :  6 * N, "nchi" : 6 * N},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" :  9 * N, "nchi" : 8 * N},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 10 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 17 * N, "nchi" : 8 * N},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  7 * N, "nchi" : 8 * N},
	# {"name" : "griewangk",   "func" : griewangk,   "npop" :  7 * N, "nchi" : 8 * N},

	# n = 20, goal = 1e-7
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * N, "nchi" : 6 * N},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 10 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 16 * N, "nchi" : 8 * N},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  6 * N, "nchi" : 8 * N},
	# {"name" : "griewangk",   "func" : griewangk,   "npop" :  6 * N, "nchi" : 8 * N},

	# n = 50, goal = 1e-7
	# {"name" : "sphere",      "func" : sphere,      "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" : 10 * N, "nchi" : 6 * N},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 11 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 16 * N, "nchi" : 8 * N},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  8 * N, "nchi" : 6 * N},
	# {"name" : "griewangk",   "func" : griewangk,   "npop" :  6 * N, "nchi" : 8 * N},

	# {"name" : "schwefel",  "func" : schwefel,  "npop" : 100 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin", "func" : rastrigin, "npop" : 16 * N, "nchi" : 8 * N},
	# {"name" : "ackley",    "func" : ackley,    "npop" : 24 * N, "nchi" : 8 * N},
	# {"name" : "griewangk", "func" : griewangk, "npop" : 11 * N, "nchi" : 8 * N},
]

for problem in PROBLEMS:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	npar = N + 1
	nchi = problem["nchi"]
	eval_counts = {}
	best_fitnesses = {}
	max_eval_count = 40000 * N
	# max_eval_count = 20000
	loop_count = 50

	print(N, name, npop, npar, nchi, loop_count, flush = True)

	for i in range(loop_count):
		method_name = "full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[npop, npar, nchi, "False"],
			],
			func,
			"random")

		result = psa.until(1e-7, max_eval_count)
		save(psa, result, method_name, name, i)

		method_name = "Npop×0.3_elite→(t=1e-2)→full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[int(npop * 0.3), npar, nchi, "self.is_stucked(1e-2)"],
				[npop, npar, nchi, "False"],
			],
			func,
			"elite")
		result = psa.until(1e-7, max_eval_count)
		save(psa, result, method_name, name, i)

		method_name = "N×3_elite→(t=1e-2)→full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[N * 3, npar, nchi, "self.is_stucked(1e-2)"],
				[npop, npar, nchi, "False"],
			],
			func,
			"elite")
		result = psa.until(1e-7, max_eval_count)
		save(psa, result, method_name, name, i)

		method_name = "N+1_elite→(t=1e-2)→full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[N + 1, npar, nchi, "self.is_stucked(1e-2)"],
				[npop, npar, nchi, "False"],
			],
			func,
			"elite")
		result = psa.until(1e-7, max_eval_count)
		save(psa, result, method_name, name, i)

	print()
	print(N, name, npop, npar, nchi, loop_count, flush = True)

	print("eval counts")
	for method_name, eval_count in eval_counts.items():
		print(
			method_name,
			np.average(eval_count),
			loop_count - len(eval_count),
			sep = ","
		)

	print()
	print("best fitnesses")
	for method_name, best_fitness in best_fitnesses.items():
		print(
			method_name,
			np.average(best_fitness),
			sep = ","
		)

	if SAVE_EVAL_COUNTS_CSV:
		for method_name, eval_count in eval_counts.items():
			filename = "benchmark/検定_{0}_{1}.csv".format(name, method_name)
			with open(filename, "w") as f:
				for x in eval_count:
					f.write("{}\n".format(x))
				f.close()

	if SAVE_BEST_FITNESSES_CSV:
		for method_name, best_fitness in best_fitnesses.items():
			filename = "benchmark/検定_{0}_{1}.csv".format(name, method_name)
			with open(filename, "w") as f:
				for x in best_fitness:
					f.write("{}\n".format(x))
				f.close()
