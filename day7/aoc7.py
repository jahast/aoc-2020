with open("aoc7.txt", "r") as f:
    raw = f.readlines()

inner_to_outer = {}
outer_to_inner = {}

for line in raw:
    stripped = line.strip()
    halves = stripped.split(" bags contain ")
    outer_bag = halves[0]
    inner_bags_strs = halves[1].split(", ")
    inners = []
    for inner_bag_str in inner_bags_strs:
        if inner_bag_str == "no other bags.":
            continue
        cleaned = inner_bag_str.replace("bags", "").replace("bag", "").replace(".", "")
        words = cleaned.strip().split(" ")
        count = int(words[0])
        bag_name = " ".join(words[1:3])
        inners.append({ "count": count, "bag": bag_name })
        inner_to_outer[bag_name] = [outer_bag] if bag_name not in inner_to_outer else inner_to_outer[bag_name] + [outer_bag]

    outer_to_inner[outer_bag] = inners


def flatten(l):
    return [item for sublist in l for item in sublist]


def recurse_out(relations, current_bags, seen):
    outer_bags = flatten([relations[current_bag] for current_bag in current_bags if current_bag in relations])
    new_bags = [outer_bag for outer_bag in outer_bags if outer_bag not in seen]
    unique_new_bags = list(set(new_bags))
    if len(unique_new_bags) == 0:
        return seen
    seen = seen + unique_new_bags
    return recurse_out(relations, unique_new_bags, seen)


def recurse_in(relations, current):
    if current not in relations:
        return 0

    inner_bags = relations[current]

    acc = 0
    for inner_bag in inner_bags:
        acc = acc + inner_bag["count"] + inner_bag["count"] * recurse_in(relations, inner_bag["bag"])

    return acc


bags = recurse_out(inner_to_outer, ["shiny gold"], ["shiny gold"])
total_bags = recurse_in(outer_to_inner, "shiny gold")

print(len(list(set(bags))))
print(total_bags)

