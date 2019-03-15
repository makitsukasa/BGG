import datetime
import numpy as np
import warnings
from jgg import JGG
from bgg import BGG
from problem.frontier.sphere      import sphere
from problem.frontier.ktablet     import ktablet
from problem.frontier.bohachevsky import bohachevsky
from problem.frontier.ackley      import ackley
from problem.frontier.schaffer    import schaffer
from problem.frontier.rastrigin   import rastrigin

warnings.simplefilter("error", RuntimeWarning)

SAVE_CSV = False

n = 20

problems = [
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * n, "nchi" : 6 * n},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" :  8 * n, "nchi" : 6 * n},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  6 * n, "nchi" : 6 * n},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  8 * n, "nchi" : 6 * n},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 10 * n, "nchi" : 8 * n},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 24 * n, "nchi" : 8 * n},
]

datestr = "{0:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())

for problem in problems:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	nchi = problem["nchi"]
	eval_counts = {}
	max_eval_count = 300000
	loop_count = 100

	print(name, loop_count)

	for i in range(loop_count):
		method_name = "JGG"
		jgg = JGG(n, npop, n + 1, nchi, func)
		result = jgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(jgg.eval_count)
			else:
				eval_counts[method_name] = [jgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_jgg_{1}_{2}.csv".format(datestr, name, i)
			with open(filename, "w") as f:
				for c, v in jgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "BGG(子数固定,加重和順)"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_sloped_rand
		result = bgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(bgg.eval_count)
			else:
				eval_counts[method_name] = [bgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_{1}_{2}_{3}.csv"\
				.format(datestr, method_name, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "BGG(子数可変,加重和順)"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_barotmetic
		bgg.select_for_reproduction = bgg.select_for_reproduction_sloped_rand
		result = bgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(bgg.eval_count)
			else:
				eval_counts[method_name] = [bgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_{1}_{2}_{3}.csv"\
				.format(datestr, method_name, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "BGG(子数固定,一部優秀)"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_partitioned
		result = bgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(bgg.eval_count)
			else:
				eval_counts[method_name] = [bgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_{1}_{2}_{3}.csv"\
				.format(datestr, method_name, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "BGG(子数可変,一部優秀)"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_barotmetic
		bgg.select_for_reproduction = bgg.select_for_reproduction_partitioned
		result = bgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(bgg.eval_count)
			else:
				eval_counts[method_name] = [bgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_{1}_{2}_{3}.csv"\
				.format(datestr, method_name, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "BGG(子数固定,親候補限)"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_restricted
		result = bgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(bgg.eval_count)
			else:
				eval_counts[method_name] = [bgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_{1}_{2}_{3}.csv"\
				.format(datestr, method_name, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		method_name = "BGG(子数可変,親候補限)"
		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_barotmetic
		bgg.select_for_reproduction = bgg.select_for_reproduction_restricted
		result = bgg.until(1e-7, max_eval_count)
		if result:
			if method_name in eval_counts:
				eval_counts[method_name].append(bgg.eval_count)
			else:
				eval_counts[method_name] = [bgg.eval_count]
		else:
			print(method_name, "failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_{1}_{2}_{3}.csv"\
				.format(datestr, method_name, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

	for method_name, counts in eval_counts.items():
		print(method_name, ":", np.average(counts))
