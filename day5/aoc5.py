from typing import List

with open("aoc5.txt", "r") as f:
    raw = f.readlines()


lines: List[str] = [line.strip() for line in raw]

ids = []

for line in lines:
    rows = list(range(0,128))
    for code in line[0:7]:
        middle = len(rows) // 2
        rows = rows[:middle] if code == "F" else rows[middle:]
    row = rows[0]

    columns = list(range(0,8))
    for code in line[-3:]:
        middle = len(columns) // 2
        columns = columns[:middle] if code == "L" else columns[middle:]

    column = columns[0]

    ids.append(row * 8 + column)

print(max(ids))
sorted_ids = sorted(ids)
for idx, ticket in enumerate(sorted_ids):
    presumed_next = ticket + 1
    if idx + 1 >= len(sorted_ids):
        continue
    if presumed_next != sorted_ids[idx + 1]:
        print(presumed_next)