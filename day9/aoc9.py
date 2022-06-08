with open("aoc9.txt", "r") as f:
    raw = f.readlines()

numbers = [int(line) for line in raw]

premaple_len = 25

ptr = premaple_len

while ptr < len(numbers):
    premaple = numbers[ptr - premaple_len:ptr]
    current = numbers[ptr]

    sums = [x + y for x in premaple for y in premaple if x != y]

    if current in sums:
        ptr += 1
        continue

    break

print(f"ptr: {ptr}, current: {current}")

forward_ptr = 1
backward_ptr = 0

while True:
    current_sum = sum(numbers[backward_ptr:forward_ptr])

    if forward_ptr - backward_ptr < 2:
        forward_ptr += 1
        continue

    if current_sum == current:
        break

    if current_sum > current:
        backward_ptr += 1
    else:
        forward_ptr += 1


series = numbers[backward_ptr:forward_ptr]

min_plus_max = min(series) + max(series)

print(f"min + max: {min_plus_max}")
