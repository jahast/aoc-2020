from enum import Enum

with open("input.txt", "r") as f:
    raw = [s.strip() for s in f.readlines()]

class Dir(Enum):
    se = 0
    sw = 1
    nw = 2
    ne = 3
    e = 4
    w = 5

offsets = {
    Dir.w: (-2, 0),
    Dir.e: (2, 0),
    Dir.ne: (1,1),
    Dir.nw: (-1, 1),
    Dir.sw: (-1, -1),
    Dir.se: (1, -1)
}

instructions = []

for row in raw:
    temp = row
    ins = []
    while len(temp) > 0:
        if temp.startswith("se"):
            ins.append(Dir.se)
            temp = temp[2:]
        elif temp.startswith("sw"):
            ins.append(Dir.sw)
            temp = temp[2:]
        elif temp.startswith("nw"):
            ins.append(Dir.nw)
            temp = temp[2:]
        elif temp.startswith("ne"):
            ins.append(Dir.ne)
            temp = temp[2:]
        elif temp.startswith("e"):
            ins.append(Dir.e)
            temp = temp[1:]
        elif temp.startswith("w"):
            ins.append(Dir.w)
            temp = temp[1:]

    instructions.append(ins)

blacks = []

for ins in instructions:
    pos = (0,0)
    for i in ins:
        offset = offsets[i]
        pos = (pos[0] + offset[0], pos[1] + offset[1])
    
    if pos in blacks:
        blacks.remove(pos)
    else:
        blacks.append(pos)

ans1 = len(blacks)

print(ans1)

def neighbours(p):
    return [(p[0] + off[0], p[1] + off[1]) for off in offsets.values()]

black_set = set(blacks)
for i in range(0,100):
    points_of_consideration = black_set
    flip_to_white = []
    flip_to_black = []
    for b in black_set:
        points_of_consideration = points_of_consideration.union(set(neighbours(b)))
    
    for p in points_of_consideration:
        nei = set(neighbours(p))
        adjacent_blacks = len(nei.intersection(black_set))
        if p in black_set:
            if adjacent_blacks == 0 or adjacent_blacks > 2:
                flip_to_white.append(p)
        else:
            if adjacent_blacks == 2:
                flip_to_black.append(p)
    
    black_set = black_set.union(flip_to_black).difference(flip_to_white)
    print(len(black_set))