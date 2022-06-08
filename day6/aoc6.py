with open("aoc6.txt", "r") as f:
    raw = f.readlines()

#part 1
answers = [[]]

for line in raw:
    cleaned = line.strip()

    if cleaned == "":
        answers.append([])
        continue

    current = answers[-1]

    for char in cleaned:
        current.append(char)


acc = 0

for ans in answers:
    acc = acc + len(set(ans))

print(acc)

#part 2
group_answers = [[]]

for line in raw:
    cleaned = line.strip()

    if cleaned == "":
        group_answers.append([])
        continue

    group_answers[-1].append(cleaned)

answer_count = 0

for group_answer in group_answers:

    individual_sets = [set(list(a)) for a in group_answer]

    acc = individual_sets.pop()

    for ans in individual_sets:
        acc = acc.intersection(ans)

    answer_count = answer_count + len(acc)


print(answer_count)