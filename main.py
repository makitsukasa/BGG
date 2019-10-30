import warnings
import numpy as np
from filemanager import mkdir, save, save_once
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

SAVE_HISTORY_CSV = True
SAVE_DISTANCE_CSV = False
SAVE_EVAL_COUNTS_CSV = False
SAVE_BEST_FITNESSES_CSV = False
DIRECTORY_NAME = "benchmark"

N = 20
# MAX_EVAL_COUNT = 40000 * N
MAX_EVAL_COUNT = 2000
LOOP_COUNT = 3

PROBLEMS = [
	# n = 20, goal = 1e-7
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * N, "nchi" : 6 * N},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" :  8 * N, "nchi" : 6 * N},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 10 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 17 * N, "nchi" : 8 * N},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  6 * N, "nchi" : 6 * N},
	# {"name" : "griewangk",   "func" : griewangk,   "npop" :  6 * N, "nchi" : 6 * N},

	# n = 50, goal = 1e-7
	# {"name" : "sphere",      "func" : sphere,      "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" : 10 * N, "nchi" : 6 * N},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  7 * N, "nchi" : 6 * N},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 11 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 16 * N, "nchi" : 8 * N},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  8 * N, "nchi" : 6 * N},
	# {"name" : "griewangk",   "func" : griewangk,   "npop" :  6 * N, "nchi" : 6 * N},

	# {"name" : "schwefel",  "func" : schwefel,  "npop" : 100 * N, "nchi" : 8 * N},
	# {"name" : "rastrigin", "func" : rastrigin, "npop" : 16 * N, "nchi" : 8 * N},
	# {"name" : "ackley",    "func" : ackley,    "npop" : 24 * N, "nchi" : 8 * N},
	# {"name" : "griewangk", "func" : griewangk, "npop" : 11 * N, "nchi" : 8 * N},
]

for problem in PROBLEMS:
	FUNC = problem["func"]
	FUNCNAME = problem["name"]
	NPOP = problem["npop"]
	NPAR = N + 1
	NCHI = problem["nchi"]
	TITLE = "_".join(map(str, [N, FUNCNAME, NPOP, NPAR, NCHI, LOOP_COUNT]))
	DIRECTORY_NAME += "/" + TITLE
	mkdir(DIRECTORY_NAME)
	eval_counts = {}
	best_fitnesses = {}
	adjust_eval_counts = {}

	print(TITLE, flush = True)

	for i in range(LOOP_COUNT):
		method_name = "full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[NPOP, NPAR, NCHI, "False"],
			],
			FUNC,
			"random")
		result = psa.until(1e-7, MAX_EVAL_COUNT)
		save(DIRECTORY_NAME, psa, result, method_name, FUNCNAME, i, best_fitnesses, adjust_eval_counts, eval_counts, SAVE_HISTORY_CSV, SAVE_DISTANCE_CSV)

		method_name = "N+1"
		psa = PopulationSizeAdjusting(
			N,
			[
				[N + 1, NPAR, NCHI, "False"],
			],
			FUNC,
			"random")
		result = psa.until(1e-7, MAX_EVAL_COUNT)
		save(DIRECTORY_NAME, psa, result, method_name, FUNCNAME, i, best_fitnesses, adjust_eval_counts, eval_counts, SAVE_HISTORY_CSV, SAVE_DISTANCE_CSV)

		method_name = "N+1→(t=1e-2)→full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[N + 1, NPAR, NCHI, "self.is_stucked(1e-2)"],
				[NPOP, NPAR, NCHI, "False"],
			],
			FUNC,
			"random")
		result = psa.until(1e-7, MAX_EVAL_COUNT)
		save(DIRECTORY_NAME, psa, result, method_name, FUNCNAME, i, best_fitnesses, adjust_eval_counts, eval_counts, SAVE_HISTORY_CSV, SAVE_DISTANCE_CSV)

		method_name = "N+1→(t=1e-3)→full"
		psa = PopulationSizeAdjusting(
			N,
			[
				[N + 1, NPAR, NCHI, "self.is_stucked(1e-3)"],
				[NPOP, NPAR, NCHI, "False"],
			],
			FUNC,
			"random")
		result = psa.until(1e-7, MAX_EVAL_COUNT)
		save(DIRECTORY_NAME, psa, result, method_name, FUNCNAME, i, best_fitnesses, adjust_eval_counts, eval_counts, SAVE_HISTORY_CSV, SAVE_DISTANCE_CSV)

	print()
	print(TITLE, flush = True)
	print("eval counts")
	for method_name, eval_count in eval_counts.items():
		print(
			method_name,
			np.average(eval_count),
			LOOP_COUNT - len(eval_count),
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
	print()
	print("switch")
	for method_name, adjust_eval_count in adjust_eval_counts.items():
		try:
			print(
				method_name,
				np.average([a for a in adjust_eval_count if a is not None]),
				sep = ","
			)
		except RuntimeWarning:
			print(
				method_name,
				"(no switch)",
				sep = ","
			)
	print()

	save_once(DIRECTORY_NAME, FUNCNAME, eval_counts, best_fitnesses, SAVE_EVAL_COUNTS_CSV, SAVE_BEST_FITNESSES_CSV)
