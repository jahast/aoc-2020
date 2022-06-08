with open("aoc13.txt", "r") as f:
    raw = f.readlines()

time = int(raw[0])
bus_lines = raw[1].split(",")
line_ids = [int(bus_line) for bus_line in bus_lines if bus_line.isdigit()]

with_wait_time = [(line_id, line_id - (time % line_id)) for line_id in line_ids]

minimum_wait = min(with_wait_time, key=lambda x: x[1])

print(minimum_wait)
print(f"part one: {minimum_wait[0] * minimum_wait[1]}")


# part 2 by sieving (god help me)
bus_lines_with_idx = list(enumerate(bus_lines))
line_ids_with_mods = [((int(x[1]) - x[0]) % int(x[1]), int(x[1])) for x in bus_lines_with_idx if x[1] != "x"]


ordered = sorted(line_ids_with_mods, key=lambda x: -x[1])

nth = 0
idx = ordered[nth][0]
addition = ordered[nth][1]
target = ordered[nth + 1][0]
mod = ordered[nth + 1][1]
target_nth = len(ordered) - 1

iter = 0

while True:
    idx += addition
    if (iter + 1) % 1000000 == 0:
        print(idx)
    mid_res = idx % mod
    if mid_res == target:
        nth += 1

        if nth == target_nth:
            break

        addition *= ordered[nth][1]
        target = ordered[nth + 1][0]
        mod = ordered[nth + 1][1]

    iter += 1

print(idx)
