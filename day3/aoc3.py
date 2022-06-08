tree = "#"

with open("aoc3.txt", "r") as f:
    raw = f.readlines()

lines = [line.strip() for line in raw]

width = len(lines[0])
height = len(lines)

x = 0
y = 0
n_trees = 0

#part 1
while True:
    if y == (height - 1):
        break

    x = x + 3
    y = y + 1

    row = lines[y]
    cell = row[x % width]

    n_trees = n_trees + 1 if cell == tree else n_trees

print(n_trees)

#part 2
x_deltas = [1,3,5,7,1]
y_deltas = [1,1,1,1,2]
n_trees_list = []

params_list = zip(x_deltas, y_deltas)

for params in params_list:
    x = 0
    y = 0
    n_trees_per_param = 0

    while True:
        if y == (height - 1):
            break

        x = x + params[0]
        y = y + params[1]

        row = lines[y]
        cell = row[x % width]

        n_trees_per_param = n_trees_per_param + 1 if cell == tree else n_trees_per_param

    n_trees_list.append(n_trees_per_param)

acc = 1
for multip in n_trees_list:
    acc = acc * multip

print(acc)