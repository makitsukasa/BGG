import numpy as np
from jgg import JGG
from bgg import BGG
from problem.frontier.sphere import sphere
from problem.frontier.ktablet import ktablet
from problem.frontier.bohachevsky import bohachevsky
from problem.frontier.ackley import ackley
from problem.frontier.schaffer import schaffer
from problem.frontier.rastrigin import rastrigin

n = 20
for problem in [sphere, ktablet, bohachevsky, ackley, schaffer, rastrigin]:
# for problem in [sphere]:
	jgg_counts = []
	bgg_counts = []

	for i in range(30):
		jgg = JGG(n, 6 * n, n + 1, 6 * n, sphere)
		jgg.until(1e-7)
		jgg_counts.append(len(jgg.history))

		bgg = BGG(n, 6 * n, n + 1, 6 * n, sphere)
		bgg.until(1e-7)
		bgg_counts.append(len(bgg.history))

	print(problem.__name__)
	print("jgg:", np.average(jgg_counts))
	print("bgg:", np.average(bgg_counts))
