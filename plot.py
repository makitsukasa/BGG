import sys
import argparse
import csv
import glob
import matplotlib.pyplot as plt
import matplotlib as mpl
from scipy import stats
import numpy as np

font = {"family": "Noto Sans MONO CJK JP"}
mpl.rc('font', **font)
plt.rcParams["mathtext.default"] = "regular"
plt.rcParams["font.size"] = 20
mpl.rc('figure.subplot', left=0.15, right=0.95, bottom=0.15, top=0.95)

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
			datas[method_name][index]["eval_count"] = list(map(int, x))
			datas[method_name][index]["fitness"] = y

	for method_name, data in datas.items():
		index = np.argmax([data[i]["eval_count"][-1] for i in range(len(data))])
		data["eval_count"] = data[index]["eval_count"]
		data["fitness"] = {}
		for i, d in data.items():
			if i == "fitness" or i == "eval_count":
				continue
			for x in data["eval_count"]:
				if not x in data["fitness"]:
					data["fitness"][x] = []
				if x in d["fitness"]:
					yindex = d["eval_count"].index(int(x))
					data["fitness"][x].append(d["fitness"][yindex])
				else:
					# Linear interpolation
					near_pin_index = np.abs(np.asarray(d["eval_count"]) - x).argsort()[:2]
					a = d["fitness"][near_pin_index[0]]
					b = d["fitness"][near_pin_index[1]]
					i_a = d["eval_count"][near_pin_index[0]]
					i_b = d["eval_count"][near_pin_index[1]]
					predicted = a + (b - a) / (i_b - i_a) * (x - i_a)
					if predicted > 1e-7:
						data["fitness"][x].append(predicted)
					else:
						# data["fitness"][x].append(1e-7)
						pass

		data["means"] = []
		data["sems"] = []
		for i, f in data["fitness"].items():
			data["means"].append(np.mean(f))
			data["sems"].append(stats.sem(f))
		plt.errorbar(
			data["eval_count"],
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
	parser = argparse.ArgumentParser()
	parser.add_argument("-f", "--files", nargs = "*")
	parser.add_argument("-l", "--log_scaled", action = "store_true")
	parser.add_argument("--ylabel", default = "評価値")
	args = parser.parse_args()
	if args.files:
		plot(args.files, args.ylabel, args.log_scaled)
	else:
		files = glob.glob('*.csv')
		plot(files, args.ylabel, args.log_scaled)
