from collections import defaultdict

with open("aoc15.txt", "r") as f:
    raw = f.readlines()

TARGET = 30000000
parsed =  [int(i) for i in raw[0].split(",")]

numbers = defaultdict(list)
for i, n in enumerate(parsed):
    numbers[n] = [i]
latest = parsed[-1]
state = (numbers, latest)

n_starting_numbers = len(numbers)

asd = [1,3,2]

for n in range(n_starting_numbers, TARGET):
    if n % 100000 == 0:
        print(n)

    c_numbers, c_latest = state

    seen_idx = c_numbers[c_latest]

    if len(seen_idx) == 1:
        c_numbers[0].append(n)
        c_latest = 0
    else:
        c_latest = seen_idx[-1] - seen_idx[-2]
        c_numbers[c_latest].append(n)

    asd.append(c_latest)
    state = (c_numbers, c_latest)

print(state[1])