import itertools

def to_chars(str: str):
    return str.strip().split(" ")

def kinda_cartesian(strs, others):
    res = []
    if len(strs) == 0:
        return others
    for one in strs:
        for other in others:
            res.append(one + other)
    return res

def compile(number, rls):

    cur = rls[number]

    if cur in ["a", "b"]:
        return [cur]

    sub_rules = rls[number].split("|")

    char_sets = [to_chars(s) for s in sub_rules]

    res = []

    for cs in char_sets:
        tmp = []
        for c in cs:
            compiled = compile(int(c), rls)
            tmp = kinda_cartesian(tmp, compiled)
        res = res + tmp
        tmp = []

    return res

with open("input.txt", "r") as f:
    raw = [s.strip() for s in f.readlines()]

raw_rules = {}

for line in itertools.takewhile(lambda x: x != "", raw):
    raw_index, raw_rule = line.split(":")
    raw_rules[int(raw_index)] = raw_rule.replace('"', "").strip()

messages = raw[(len(raw_rules) + 1):]

compiled_rules = {key: compile(key, raw_rules) for key in raw_rules.keys()}

first_rule = compiled_rules[0]

ans1 = 0
for mes in messages:
    ans1 = ans1 + 1 if mes in first_rule else ans1

print(ans1)

ans2 = 0
for mes in messages:
    tmp = mes
    multiple_31_len = len(compiled_rules[31][0])
    multiple_42_len = len(compiled_rules[42][0])

    how_many_42s = 0
    while True:
        if tmp.startswith(tuple(compiled_rules[42])):
            how_many_42s += 1
            tmp = tmp[multiple_42_len:] if multiple_42_len < len(tmp) else ""
        else:
            break

    how_many_31s = 0
    while True:
        if tmp.startswith(tuple(compiled_rules[31])) or tmp in compiled_rules[31]:
            how_many_31s += 1
            tmp = tmp[multiple_31_len:] if multiple_31_len < len(tmp) else ""
        else:
            break

    if tmp == "" and how_many_31s > 0 and how_many_42s > 0 and how_many_42s > how_many_31s:
        ans2 +=1

print(ans2)