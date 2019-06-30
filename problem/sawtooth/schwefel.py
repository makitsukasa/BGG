import numpy as np

def schwefel(x):
	shifted = x * 1000 - 500
	return np.sum(-shifted * np.sin(np.sqrt(abs(shifted)))) + 418.982887272432744946 * len(x)

# https://www.wolframalpha.com/input/?i=Minimize%5B%7B-x+Sin%5BSqrt%5BAbs%5Bx%5D%5D%5D,+Abs%5Bx%5D+%3C+500%7D,+%7Bx%7D%5D
# NumberForm[Minimize[{(-x) Sin[Sqrt[Abs[x]]], Abs[x] < 500}, {x}], 52]
# NumberForm[(-420.9687435998202731185) Sin[Sqrt[Abs[420.9687435998202731185]]], 50]
# print(schwefel(np.array([(420.9687435998202731185 + 500) / 1000 for _ in range(10)])))
