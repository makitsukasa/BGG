import numpy as np

def schwefel(x):
	shifted = x * 1000 - 500
	# print(shifted)
	# print(- shifted * np.sin(np.sqrt(abs(shifted))))
	# ans = 0
	# for i in range(len(x)):
	# 	print(-shifted[i] * np.sin(np.sqrt(abs(shifted[i]))))
	# 	ans += 418.982887272432744946 - shifted[i] * np.sin(np.sqrt(abs(shifted[i])))
	# if ans < 0:
	# 	print("---------------------------------------------------------------------------------------")
	# 	print(x)
	# 	print(shifted)
	# 	print(ans)
	# 	print("---------------------------------------------------------------------------------------")
	# 	pass
	# return ans
	return 418.982887272432744946 * len(x) - np.sum(shifted * np.sin(np.sqrt(np.abs(shifted))))

# https://www.wolframalpha.com/input/?i=Minimize%5B%7B-x+Sin%5BSqrt%5BAbs%5Bx%5D%5D%5D,+Abs%5Bx%5D+%3C+500%7D,+%7Bx%7D%5D
# NumberForm[Minimize[{(-x) Sin[Sqrt[Abs[x]]], Abs[x] < 500}, {x}], 52]
# NumberForm[(-420.9687435998202731185) Sin[Sqrt[Abs[420.9687435998202731185]]], 50]
# (420.9687435998202731185 + 500) / 1000
# print(schwefel(np.array([0.9209687435998202731185 for _ in range(10)])))
# print(schwefel(np.array([ 0.21363712 , 1.20304801, -0.48700694, -0.82583672, -0.01532567, -0.44955003,  0.30462951, -0.392422, -0.89743887,  0.67653174])))
