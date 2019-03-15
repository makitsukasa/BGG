import sys
import argparse
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl

font = {"family": "Noto Sans MONO CJK JP"}
mpl.rc('font', **font)
plt.rcParams["mathtext.default"] = "regular"

def plot(filenames, log_scaled = False):
	if isinstance(filenames, str):
		filenames = [filenames]

	for filename in filenames:
		with open(filename, "r") as f:
			x = []
			y = []
			reader = csv.reader(f, quoting = csv.QUOTE_NONNUMERIC)
			for row in reader:
				x.append(row[0])
				y.append(row[1])
			plt.plot(x, y, linewidth = 0.5, label = filename.split("\\")[-1].split(".")[0])

	if log_scaled:
		plt.yscale("log")
	plt.legend()
	plt.show()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		parser = argparse.ArgumentParser()
		parser.add_argument("-f", "--files", nargs = "*")
		parser.add_argument("-l", "--log_scaled", action = "store_true")
		args = parser.parse_args()
		plot(args.files, args.log_scaled)
	else:
		plot([
			"benchmark\\JGG.csv",
			"benchmark\\BGG(子個体数固定，親加重和順).csv",
			"benchmark\\BGG(子個体数可変，親加重和順).csv",
		])
