with open("aoc8.txt", "r") as f:
    raw = f.readlines()

instructions = []

for line in raw:
    items = line.rstrip().split(" ")
    instructions.append((items[0], int(items[1])))

def execute(isntr):
    ptr = 0
    acc = 0
    seen = []
    finished = False

    while True:
        if ptr in seen:
            break
        if ptr == len(isntr):
            finished = True
            break
        seen.append(ptr)

        row = isntr[ptr]
        instrction = row[0]
        quantity = row[1]

        if instrction == "nop":
            ptr += 1
            continue
        elif instrction == "acc":
            acc += quantity
            ptr += 1
            continue
        elif instrction == "jmp":
            ptr += quantity
            continue

    return finished, acc, seen

_, acc, seen = execute(instructions)
print(acc)


for seen_row_index in seen:
    modified_instructions = instructions.copy()
    seen_row = modified_instructions[seen_row_index]

    if seen_row[0] in ["nop", "jmp"]:
        new_instr = "nop" if seen_row[0] == "jmp" else "jmp"
        modified_instructions[seen_row_index] = (new_instr, seen_row[1])
        fin, acc, _ = execute(modified_instructions)

        if fin:
            print(acc)
