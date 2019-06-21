import warnings
import numpy as np
from PopulationSizeAdjusting import PopulationSizeAdjusting
from SawTooth import SawTooth
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

SAVE_HISTORY_CSV = False
SAVE_DISTANCE_CSV = False
SAVE_COUNTS_CSV = True

N = 20

PROBLEMS = [
	{"name" : "sphere",      "func" : sphere,      "npop" :  7 * N, "nchi" : 6 * N},
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
	eval_counts = {}
	max_eval_count = 400000
	loop_count = 1

	print(name, loop_count, flush = True)

	for i in range(loop_count):
		# method_name = "full"
		# psa = PopulationSizeAdjusting(
		# 	N,
		# 	[[npop, npar, nchi, "False"]],
		# 	func)
		# result = psa.until(1e-7, max_eval_count)
		# save(psa, result, method_name, name, i)

		# method_name = "full→(t=1e-2)→0.7full"
		# psa = PopulationSizeAdjusting(
		# 	N,
		# 	[
		# 		[npop, npar, nchi, "self.is_stucked(1e-6)"],
		# 		[int(npop * 0.7), npar, nchi, "False"],
		# 	],
		# 	func)
		# result = psa.until(1e-7, max_eval_count)
		# save(psa, result, method_name, name, i)

		method_name = "sawtooth"
		st = SawTooth(
			N,
			npop,
			int(0.8 * npop),
			npar,
			nchi,
			40,
			func)
		result = st.until(1e-7, max_eval_count)
		save(st, result, method_name, name, i)

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
