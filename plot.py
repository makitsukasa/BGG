import sys
import argparse
import csv
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import numpy as np

font = {"family": "Noto Sans MONO CJK JP"}
mpl.rc('font', **font)
plt.rcParams["mathtext.default"] = "regular"

def plot(filenames, ylabel, log_scaled = False):
	if isinstance(filenames, str):
		filenames = [filenames]

	datas = {}
	for filename in filenames:
		with open(filename, "r") as f:
			x = []
			y = []
			reader = csv.reader(f, quoting = csv.QUOTE_NONNUMERIC)
			for row in reader:
				x.append(row[0])
				y.append(row[1])
			base_file_name = filename.split("\\")[-1].replace(".csv", "")
			method_name = "_".join(base_file_name.split("_")[:-1])
			index = int(base_file_name.split("_")[-1])
			if not method_name in datas:
				datas[method_name] = {}
			datas[method_name][index] = {}
			datas[method_name][index]["x"] = list(map(lambda i: int(i), x))
			datas[method_name][index]["y"] = y

	for method_name, data in datas.items():
		data["raw_datas"] = {}
		for i, d in data.items():
			if i == "raw_datas":
				continue
			for xindex in data[0]["x"]:
				if not xindex in data["raw_datas"]:
					data["raw_datas"][xindex] = []
				if index in data["raw_datas"]:
					yindex = d["x"].index(int(xindex))
					data["raw_datas"][xindex].append(d["y"][yindex])
				else:
					# Linear interpolation
					near_pin_index = np.abs(np.asarray(d["x"]) - xindex).argsort()[:2]
					a = d["y"][near_pin_index[0]]
					b = d["y"][near_pin_index[1]]
					i_a = d["x"][near_pin_index[0]]
					i_b = d["x"][near_pin_index[1]]
					data["raw_datas"][xindex].append(
						a + (b - a) / (i_b - i_a) * (xindex - i_a))
		data["means"] = []
		data["sems"] = []
		for xindex, d in data["raw_datas"].items():
			data["means"].append(np.mean(d))
			data["sems"].append(stats.sem(d))
		plt.errorbar(
			data[0]["x"],
			data["means"],
			yerr = data["sems"],
			label = method_name)

	if log_scaled:
		plt.yscale("log")
	plt.legend()
	plt.xlabel("評価回数")
	plt.ylabel(ylabel)
	plt.show()

if __name__ == '__main__':
	if len(sys.argv) > 1:
		parser = argparse.ArgumentParser()
		parser.add_argument("-f", "--files", nargs = "*")
		parser.add_argument("-l", "--log_scaled", action = "store_true")
		parser.add_argument("--ylabel", default = "評価値")
		args = parser.parse_args()
		plot(args.files, args.ylabel, args.log_scaled)
	else:
		plot([
			"benchmark\\JGG.csv",
			"benchmark\\BGG(子個体数固定，親加重和順).csv",
			"benchmark\\BGG(子個体数可変，親加重和順).csv",
		])
