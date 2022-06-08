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
    binary_pres = list("{0:036b}".format(int(addr)))

    masked = []
    for addr_val, mask_val in zip(binary_pres, mask):
        if mask_val == "0":
            masked.append(addr_val)
        else:
            masked.append(mask_val)

    n_floating = len([i for i in masked if i == "X"])
    replacers = itertools.product(*[["0","1"] for l in range(0,n_floating)])

    for rep in replacers:
        replaced = "".join(masked).replace("X", "{}").format(*rep)
        mem[int(replaced, 2)] = int(val)
    

acc = sum([v for v in mem.values()])
print(acc)