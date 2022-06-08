from math import sqrt

with open("input.txt", "r") as f:
    raw = [s.strip() for s in f.readlines() if s.strip() != ""]

chunked = [raw[i:(i + 11)] for i in range(0, len(raw), 11)]

tiles = {int(s[0][5:9]): s[1:] for s in chunked}

def sides(tile):
    left = [tile[i][0] for i in range(0,len(tile))]
    right = [tile[i][-1] for i in range(0,len(tile))]
    return [list(tile[0]), right, list(tile[-1]), left]

def all_sides(tile):
    sidess = sides(tile)
    return sidess + [s[::-1] for s in sidess]

found = []
for i in tiles.keys():
    candidate_tile = tiles[i]
    others = [j for j in tiles.keys() if j != i]
    candidate_sides = sides(candidate_tile)
    side_matches = [False, False, False, False]
    for j in others:
        other_sides = all_sides(tiles[j])

        if candidate_sides[0] in other_sides:
            side_matches[0] = True

        if candidate_sides[1] in other_sides:
            side_matches[1] = True

        if candidate_sides[2] in other_sides:
            side_matches[2] = True

        if candidate_sides[3] in other_sides:
            side_matches[3] = True

    if sum(side_matches) == 2:
        found.append(i)

ans1 = found[0] * found[1] * found[2] * found[3]
print(ans1)

# it was a good try to cheat this problem :'D

def rotate(tile):
    force_list = [list(r) for r in tile]
    new = []
    for j in range(0,len(force_list[0])):
        new += [[force_list[i][j] for i in range(len(force_list) - 1,-1,-1)]]
    return new

def flip(tile):
    force_list = [list(r) for r in tile]
    return [r[::-1] for r in force_list]

side_length = int(sqrt(len(tiles)))
solved = {}
solved_tiles = [[] for _ in range (0,len(tiles))]

OUTER_RIM = -99
NOT_KNOWN = -98

for i in range(0, len(tiles)):
    if i in solved:
        continue

    neighbours_idxs = [
        i - side_length, 
        i + 1 if (i + 1) // side_length == i // side_length else -1, 
        i + side_length,
        i - 1 if (i - 1) // side_length == i // side_length else -1
    ]

    filtered_idxs = []
    for j in neighbours_idxs:
        if j in solved:
            filtered_idxs.append(j)
        elif j < 0 or j >= len(solved_tiles):
            filtered_idxs.append(OUTER_RIM)
        else:
            filtered_idxs.append(NOT_KNOWN)

    if all(fi == NOT_KNOWN for fi in filtered_idxs):
        continue

    not_solved = [c for c in tiles if c not in solved.values()]

    for candidate in not_solved:
        candidate_tile = tiles[candidate]

        others = [t for t in tiles if t != candidate and t in not_solved]

        for rot in range(0,8):
            if rot == 4:
                candidate_tile = flip(candidate_tile)
            candidate_tile = rotate(candidate_tile)
            candidate_sides = sides(candidate_tile)

            is_match = True
            for side_idx, (side, nei) in enumerate(zip(candidate_sides, filtered_idxs)):
                if nei == OUTER_RIM:
                    for o in others:
                        is_match = is_match and side not in all_sides(tiles[o])
                elif nei == NOT_KNOWN:
                    continue
                else:
                    neighbour = solved_tiles[nei]
                    is_match = is_match and side == sides(neighbour)[((side_idx + 2) % 4)]

            if is_match:
                solved_tiles[i] = candidate_tile
                solved[i] = candidate
                break

        if is_match:
            break

    if not is_match:
        break
# combine the tiles
def remove_border(tile):
    return [r[1:-1] for r in tile][1:-1]

borderless_tiles = [remove_border(t) for t in solved_tiles]

whole_picture = []
for mr in range(0, len(solved), side_length):
    for r in range(0,8):
        new_row = []
        for addition in range(0, side_length):
            new_row += borderless_tiles[mr + addition][r]
        whole_picture += [new_row]

# represent the monster as offsets where the #s are
with open("fish.txt", "r") as f:
    raw = [s for s in f.readlines()]

fish = [list(r.replace("\n", "")) for r in raw]

offsets = [[i,j] for i in range(0, len(fish)) for j in range(0, len(fish[0])) if fish[i][j] == "#"]

# brute force the monsters
possible_monster_start_poss = [[i,j] for i in range(0, len(whole_picture) - 2) for j in range(0, len(whole_picture[0]) - 19)]
matches = 0
for rot in range(0,8):
    if rot == 4:
        whole_picture = flip(whole_picture)
    whole_picture = rotate(whole_picture)
    for p in possible_monster_start_poss:
        match = all([whole_picture[p[0] + of[0]][p[1] + of[1]] == "#" for of in offsets])
        if match:
            matches += 1

    if matches > 0:
        break

all_hashes = sum([c == "#" for row in whole_picture for c in row])
hashes_in_fish = sum([c == "#" for row in fish for c in row])
ans2 = all_hashes - matches * hashes_in_fish
print(ans2)

