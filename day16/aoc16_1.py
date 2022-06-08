import itertools
import re

def make_fun(a,b,c,d):
    return lambda x: a <= x <= b or c <= x <= d

with open("aoc16.txt", "r") as f:
    raw = f.readlines()

lines = iter([line.strip() for line in raw])

constraints = []

for line in itertools.takewhile(lambda x: x != "", lines):
    name, raw_contraints = line.split(":")
    nums = [int(i) for i in re.findall(r"\d+", raw_contraints)]
    fun = make_fun(*nums)
    constraints.append((name, fun))

my_ticket = []

for line in itertools.takewhile(lambda x: x != "", lines):
    if line == "your ticket:":
        continue

    my_ticket = [int(x) for x in line.split(",")]

nearby_tickets = []

for line in itertools.takewhile(lambda x: x != "", lines):
    if line == "nearby tickets:":
        continue

    ticket = [int(x) for x in line.split(",")]
    nearby_tickets.append(ticket)

invalids = []
valid_tickets = []

all_funs = [fun for _, fun in constraints]

for ticket in nearby_tickets:
    is_valid = True
    for val in ticket:
        if not any([fun(val) for fun in all_funs]):
            invalids.append(val)
            is_valid = False
            break
    
    if is_valid:
        valid_tickets.append(ticket)

print(sum(invalids))

transposed = []
funs_per_idx = []
for i in range(0, len(constraints)):
    vals = [l[i] for l in valid_tickets]
    valid_funs = [(name,fun) for name, fun in constraints if all([fun(j) for j in vals])]
    funs_per_idx = funs_per_idx + [valid_funs]
    transposed.append([l[i] for l in valid_tickets])

indexed = list(enumerate(funs_per_idx))

sorted_order = sorted(indexed, key=lambda x: len(x[1]))

def figure_it_out(i, allocated):

    if i == len(constraints):
        return allocated

    allocated_names = [n for n, _ in allocated]

    good_funs = sorted_order[i][1]
    this_idx = sorted_order[i][0]

    left = [(name,this_idx) for name, _ in good_funs if name not in allocated_names ]

    if len(left) == 0:
        return None

    for gf in left:
        ret = figure_it_out(i+1, allocated + [gf])
        if ret != None:
            return ret

ticket_fields_in_order = figure_it_out(0,[])

departure_fields_idxs = [idx for name,idx in ticket_fields_in_order if name.startswith("departure") ]

my_ticket_vals = [my_ticket[i] for i in departure_fields_idxs]

acc = 1
for val in my_ticket_vals:
    acc *= val

print(acc)