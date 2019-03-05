import numpy as np
from jgg import JGG
from bgg import BGG
import warnings
from problem.frontier.sphere import sphere
from problem.frontier.ktablet import ktablet
from problem.frontier.bohachevsky import bohachevsky
from problem.frontier.ackley import ackley
from problem.frontier.schaffer import schaffer
from problem.frontier.rastrigin import rastrigin

warnings.simplefilter("error", RuntimeWarning)

n = 20

problems = [
	{"name" : "sphere",      "func" : sphere,      "npop" :  6 * n, "nchi" : 6 * n},
	# {"name" : "k-tablet",    "func" : ktablet,     "npop" :  8 * n, "nchi" : 6 * n},
	# {"name" : "bohachevsky", "func" : bohachevsky, "npop" :  6 * n, "nchi" : 6 * n},
	# {"name" : "ackley",      "func" : ackley,      "npop" :  8 * n, "nchi" : 6 * n},
	# {"name" : "schaffer",    "func" : schaffer,    "npop" : 10 * n, "nchi" : 8 * n},
	# {"name" : "rastrigin",   "func" : rastrigin,   "npop" : 24 * n, "nchi" : 8 * n},
]

for problem in problems:
	func = problem["func"]
	name = problem["name"]
	npop = problem["npop"]
	nchi = problem["nchi"]
	jgg_counts = []
	bgg_counts = []

	print(name)

	for i in range(100):
		seed = 1039522760
		# seed = 1439646204
		np.random.seed(seed)
		jgg = JGG(n, npop, n + 1, nchi, func)
		np.random.seed()
		result = jgg.until(1e-7, 300000 // nchi)
		if result:
			jgg_counts.append(len(jgg.history))
		else:
			print("jgg failed")
			print("seed :", seed)

		bgg = BGG(n, npop, n + 1, nchi, func)
		result = bgg.until(1e-7, 300000 // nchi)
		if result:
			bgg_counts.append(len(bgg.history))
		else:
			print("bgg failed")

	print("jgg:", np.average(jgg_counts))
	print("bgg:", np.average(bgg_counts))
