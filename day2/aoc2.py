from typing import List

with open("aoc2.txt", "r") as f:
    lines = f.readlines()

matches = 0
mathces_part_two = 0

for line in lines:
    splitted = line.split(":")
    constraint: str = splitted[0]
    password: str = splitted[1].strip()

    constraint_splitted = constraint.split(" ")
    limits: List[int] = [int(i) for i in constraint_splitted[0].split("-")]
    character = constraint_splitted[1]

    # part 1
    n_characters = password.count(character)
    if n_characters >= limits[0] and n_characters <= limits[1]:
        matches = matches + 1

    # part 2
    positions = [i - 1 for i in limits]
    if (password[positions[0]] == character) ^ (password[positions[1]] == character):
        mathces_part_two = mathces_part_two + 1

print(matches)
print(mathces_part_two)