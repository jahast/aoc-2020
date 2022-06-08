
with open("aoc1.txt", "r") as f:
    lines = f.readlines()

numbers = [int(i) for i in lines]

for i in numbers:
    for j in numbers:
        for k in numbers:

            if i == j or i == k or j == k:
                continue

            if i + j + k == 2020:
                print(f"answer:{i * j * k}")
                break