import os

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def mkdir(path):
	if os.path.exists(path):
		entries = os.listdir(path)
		if entries:
			raise Exception(path + " already exists and is not an empty directory")
		# else:
		# 	pass # do nothing
	else:
		os.mkdir(path)

def save(path, system, result, method_name, problem_name, index, best_fitnesses, adjust_eval_counts, eval_counts, SAVE_HISTORY_CSV, SAVE_DISTANCE_CSV):
	if method_name in best_fitnesses:
		best_fitnesses[method_name].append(system.get_best_fitness())
	else:
		best_fitnesses[method_name] = [system.get_best_fitness()]

	if method_name in adjust_eval_counts:
		adjust_eval_counts[method_name].append(system.get_adjust_eval_count()[0])
	else:
		adjust_eval_counts[method_name] = [system.get_adjust_eval_count()[0]]

	if result:
		if method_name in eval_counts:
			eval_counts[method_name].append(system.eval_count)
		else:
			eval_counts[method_name] = [system.eval_count]
	else:
		print(method_name, "failed")

	# print(system.population[0].gene)

	if SAVE_HISTORY_CSV:
		filename = path + "/{0}_{1}_{2}.csv"\
			.format(method_name, problem_name, index)
		with open(filename, "w") as f:
			for c, v in system.history.items():
				f.write("{0},{1}\n".format(c, v))
			f.close()
	if SAVE_DISTANCE_CSV:
		filename = path + "/距離_{0}_{1}_{2}.csv"\
			.format(method_name, problem_name, index)
		with open(filename, "w") as f:
			for c, v in system.mean_of_distance_history.items():
				f.write("{0},{1}\n".format(c, v))
			f.close()

def save_once(path, method_name, eval_counts, best_fitnesses, SAVE_EVAL_COUNTS_CSV, SAVE_BEST_FITNESSES_CSV):
	if SAVE_EVAL_COUNTS_CSV:
		for method_name, eval_count in eval_counts.items():
			filename = path + "/検定_{0}_{1}.csv".format(FUNCNAME, method_name)
			with open(filename, "w") as f:
				for x in eval_count:
					f.write("{}\n".format(x))
				f.close()

	if SAVE_BEST_FITNESSES_CSV:
		for method_name, best_fitness in best_fitnesses.items():
			filename = path + "/検定_{0}_{1}.csv".format(FUNCNAME, method_name)
			with open(filename, "w") as f:
				for x in best_fitness:
					f.write("{}\n".format(x))
				f.close()
