with open("aoc15.txt", "r") as f:
    raw = f.readlines()

def rindex(l, val):
    return len(l) - l[::-1].index(val) - 1

TARGET = 2020

numbers = [int(n) for n in raw[0].split(",")]

n_starting_numbers = len(numbers)

for n in range(n_starting_numbers, TARGET):
    last_number = numbers[-1]
    initial = numbers[0:-1]

    if last_number in initial:
        found_idx = rindex(initial, last_number)
        numbers.append((n - 1) - found_idx)
    else:
        numbers.append(0)

print(len(numbers))
print(numbers[-1])