import itertools
import re
from collections import defaultdict

# I actually couldn't figure out an easier way to solve the first part
# and I assume there was one by the way the problem was phrased and because 
# I instantly got the answer to the second part as well
with open("input.txt", "r") as f:
    raw = [s.strip() for s in f.readlines()]

input = []
for l in raw:
    ingreds_raw = re.search('(.*) \(', l).group(0)
    ingreds = ingreds_raw.replace("(", "").strip().split(" ")

    allergens_raw = re.search('\(.*\)', l).group(0)
    allergens_splat = allergens_raw[1:-1].replace("contains", "").strip().split(",")
    allergens = [a.strip() for a in allergens_splat]
    input.append((ingreds, allergens))


match_dict = defaultdict(list)

for inger, aller in input:
    for a in aller:
        if match_dict[a] == []:
            match_dict[a] = inger
        else:
            match_dict[a] = list(set(match_dict[a]).intersection(set(inger)))

while any(len(v) != 1 for v in match_dict.values()):
    for k, v in match_dict.items():
        if len(v) != 1:
            continue
        val_to_remove = v[0]
        for kk, vv in match_dict.items():
            if kk == k or len(vv) == 1:
                continue

            match_dict[kk] = [val for val in vv if val != val_to_remove]

ingreds_with_allergens = [v[0] for v in match_dict.values()]

all_occurences = list(itertools.chain(*[a[0] for a in input]))

ans1 = sum(a not in ingreds_with_allergens for a in all_occurences)

print(ans1)

tuple_matches = [(k,v[0]) for k,v in match_dict.items()]
sorted_by_allergen = sorted(tuple_matches, key=lambda x: x[0])
ans2 = ",".join([v for _,v in sorted_by_allergen])

print(ans2)