input = "186524973"

table = [int(i) for i in input]

def find_index(ls, val):
    for i in range(max(len(ls) - 1000,0), len(ls)):
        if val == ls[i]:
            return i
    return ls.index(val)

def run(new, runs):
    i = 0
    tlen = len(new)
    while i < runs:
        table = new
        cur = table[0]
        to_pick_up = [n for n in [1,2,3]]
        picked_up = [table[j] for j in to_pick_up]
        dest_value = (cur - 2) % tlen + 1
        while True:
            dest_idx = table.index(dest_value)
            if dest_idx not in to_pick_up:
                break
            dest_value = (dest_value - 2) % tlen + 1

        new = table[4:(dest_idx + 1)]
        new.extend(picked_up)
        new.extend(table[(dest_idx + 1):])
        new.append(table[0])

        i += 1
        cur = (cur + 1) % tlen

    return new

ans1_res = run(table, 100)

index_of_one = ans1_res.index(1)

ans1 = "".join(str(ans1_res[((k + index_of_one) % 9)]) for k in range(1,9))

print(ans1)

# tbh I couldn't figure this out on my own
# although I didn't copy this from everywhere I did google the method

def better_run(d, runs, start):
    i = 0
    dmin, dmax = 0, len(d)
    cur = start
    while i < runs:
        next_4 = []
        next_cup = cur
        for _ in range(0,4):
            next_cup = d[next_cup]
            next_4.append(next_cup)
        
        *picked_up, after_pick_up = next_4
        
        dest_val = cur - 1
        while dest_val in picked_up or dest_val == dmin:
            if dest_val == dmin:
                dest_val = dmax
            else:
                dest_val -= 1

        d[cur] = after_pick_up
        d[picked_up[-1]] = d[dest_val]
        d[dest_val] = picked_up[0]

        cur = after_pick_up

        i += 1
        # if i % 100000 == 0:
        #     print(i)

    return d

table2 = [int(i) for i in input] + list(range(10,1000001))
d = {table2[i]:table2[i + 1] for i in range(0, 1000000 - 1)}
d[table2[-1]] = table[0]

res = better_run(d, 10000000, int(input[0]))

ans2 = res[1] * res[res[1]]
print(ans2)