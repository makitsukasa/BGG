import sys
import csv
import matplotlib.pyplot as plt

def plot(filenames):
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
			plt.plot(x, y, linewidth = 0.5)

	plt.yscale("log")
	plt.show()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		plot(sys.argv[1:])
	else:
		plot([
			"benchmark/2019-03-10_03-13-11.csv",
			"benchmark/2019-03-10_03-13-20.csv",
		])
