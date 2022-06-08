with open("aoc10.txt", "r") as f:
    raw = f.readlines()

jolts_ordered = sorted([int(line) for line in raw])

difference_counts = {
    1: 0,
    2: 0,
    3: 0
}

pairs = [(x,y) for x,y in zip(jolts_ordered, jolts_ordered[1:])]

for pair in pairs:
    diff = pair[1] - pair[0]
    difference_counts[diff] += 1

difference_counts[jolts_ordered[0]] += 1
difference_counts[3] += 1

print(difference_counts[1] * difference_counts[3])

def recurse(jolts, ptr, mem):
    if ptr in mem:
        return mem[ptr]

    if ptr == len(jolts) - 1:
        return 1

    current = jolts[ptr]
    next_candidate_indices = list(range(ptr+1, ptr+4))
    next_cadidates = zip(next_candidate_indices, jolts[ptr+1:ptr+4])

    acc = 0
    for candidate in next_cadidates:
        if candidate[1] - current <= 3:
            acc += recurse(jolts, candidate[0], mem)

    mem[ptr] = acc
    return acc

mem = {}
count = recurse([0] + jolts_ordered, 0, mem)

print(count)
