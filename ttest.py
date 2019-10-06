import sys
import glob
import csv
import numpy as np
from scipy import stats

def ttest(filenames, log_scaled = False):
	if isinstance(filenames, str):
		print("give 2 or more files")
		exit(-1)

	datas = {}

	for filename in filenames:
		with open(filename, "r") as f:
			x = []
			y = []
			reader = csv.reader(f, quoting = csv.QUOTE_NONNUMERIC)
			datas[filename] = [x for x in reader]
		print(filename.split("\\")[-1].replace(".csv", ","), np.mean(datas[filename]))
	print()

	for filename in filenames:
		print(",", filename.split("\\")[-1].replace(".csv", ""), end = "")
	print()

	for i in range(len(filenames)):
		print(filenames[i].split("\\")[-1].replace(".csv", ""), end = ",")
		for j in range(len(filenames)):
			result = stats.ttest_ind(datas[filenames[i]], datas[filenames[j]])
			if result.pvalue < 0.05:
				# 有意差あり
				print("◯ " if result.statistic[0] < 0 else "✕ ", end = "")
			else:
				# 有意差なし
				print("- ", end = "")
			print("({0:.3f}),".format(result.pvalue[0]), end = "")

		print()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		ttest(sys.argv[1:])
	else:

		files = glob.glob('*.csv')
		ttest(files)
