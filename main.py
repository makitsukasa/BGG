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
	{"name" : "k-tablet",    "func" : ktablet,     "npop" :  8 * n, "nchi" : 6 * n},
	{"name" : "bohachevsky", "func" : bohachevsky, "npop" :  6 * n, "nchi" : 6 * n},
	{"name" : "ackley",      "func" : ackley,      "npop" :  8 * n, "nchi" : 6 * n},
	{"name" : "schaffer",    "func" : schaffer,    "npop" : 10 * n, "nchi" : 8 * n},
	{"name" : "rastrigin",   "func" : rastrigin,   "npop" : 24 * n, "nchi" : 8 * n},
]

datestr = "{0:%Y-%m-%d_%H-%M-%S}".format(datetime.datetime.now())

for problem in problems:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	nchi = problem["nchi"]
	jgg_counts = []
	bgg_barometric_counts = []
	bgg_fixed_counts = []

	print(name)

	for i in range(1):
		jgg = JGG(n, npop, n + 1, nchi, func)
		result = jgg.until(1e-7, 300000)
		if result:
			jgg_counts.append(jgg.eval_count)
		else:
			print("jgg failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_jgg_{1}_{2}.csv".format(datestr, name, i)
			with open(filename, "w") as f:
				for c, v in jgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_fixed
		bgg.select_for_reproduction = bgg.select_for_reproduction_sloped_rand
		result = bgg.until(1e-7, 300000)
		if result:
			bgg_fixed_counts.append(bgg.eval_count)
		else:
			print("bgg (nchi:fixed,repr:slope) failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_bgg_b_{1}_{2}.csv".format(datestr, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

		bgg = BGG(n, npop, n + 1, nchi, func)
		bgg.get_nchi = bgg.get_nchi_barotmetic
		bgg.select_for_reproduction = bgg.select_for_reproduction_sloped_rand
		result = bgg.until(1e-7, 300000)
		if result:
			bgg_barometric_counts.append(bgg.eval_count)
		else:
			print("bgg (nchi:barom,repr:slope) failed")

		if SAVE_CSV:
			filename = "benchmark/{0}_bgg_f_{1}_{2}.csv".format(datestr, name, i)
			with open(filename, "w") as f:
				for c, v in bgg.history.items():
					f.write("{0},{1}\n".format(c, v))
				f.close()

	print("jgg:", np.average(jgg_counts))
	print("bgg_fixed:", np.average(bgg_fixed_counts))
	print("bgg_barometric:", np.average(bgg_barometric_counts))
