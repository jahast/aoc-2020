import re
import itertools


with open("aoc14.txt", "r") as f:
    raw = f.readlines()

instructions = [line.strip() for line in raw]
mask = []
mem = {}

for ins in instructions:
    if ins.startswith("mask"):
        mask = list(ins.split("=")[1].strip())
        continue

    addr, val = re.findall(r"\d+", ins)
    binary_pres = list("{0:036b}".format(int(val)))

    masked = []
    for val, mask_val in zip(binary_pres, mask):
        if mask_val == "X":
            masked.append(val)
        else:
            masked.append(mask_val)
    
    masked_int_val = int("".join(masked), 2)
    mem[addr] = masked_int_val


acc = sum([v for v in mem.values()])
print(acc)