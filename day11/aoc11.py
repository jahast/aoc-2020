
with open("aoc11.txt", "r") as f:
    raw = f.readlines()

def safe_get(arr, i, j):
    if i < 0 or j < 0:
        return None
    elif i >= len(arr):
        return None
    row = arr[i]
    if j >= len(row):
        return None
    
    return row[j]

def adjacent(arr, i, j):
    opers = [-1, 0, 1]
    neighbours_idxs = [(i + ii,j + jj) for ii in opers for jj in opers if ii !=0 or jj != 0]
    neighbours = [safe_get(arr, ii, jj) for ii,jj in neighbours_idxs]
    return [n for n in neighbours if n is not None]

def adjacent_2(arr, i, j):
    directions = [-1, 0, 1]
    vectors = [(ii,jj) for ii in directions for jj in directions if ii !=0 or jj != 0]
    adj = []
    for vector in vectors:
        ii, jj = i, j
        while True:
            ii, jj = (ii + vector[0], jj + vector[1])
            new_loc = safe_get(arr, ii, jj)
            if new_loc in ["L", "#"]:
                adj.append(new_loc)
                break
            if new_loc is None:
                break

    return adj

def solve(arr, adjacent_fun, thres):
    while True:
        change_set = []
        for i, row in enumerate(arr):
            for j, cell in enumerate(row):
                adj = adjacent_fun(arr, i, j)
                if cell == ".":
                    continue
                elif cell == "L":
                    if "#" not in adj:
                        change_set.append((i,j,"#"))
                    continue
                elif cell == "#":
                    reserved_count = len([c for c in adj if c == "#"])
                    if reserved_count >= thres:
                        change_set.append((i,j,"L"))
                    continue
                
                raise Exception() 

        if len(change_set) == 0:
            break

        for change in change_set:
            arr[change[0]][change[1]] = change[2]

    return arr

def count_occupied(arr):
    occupied = 0
    for r in arr:
        for c in r:
            if c == "#":
                occupied += 1
    return occupied


matrix = [list(line.strip()) for line in raw]

initial_1 = [line.copy() for line in matrix]
solved_1 = solve(initial_1, adjacent, 4)
print(f"task 1: {count_occupied(solved_1)}")

initial_2 = [line.copy() for line in matrix]
solved_2 = solve(initial_2, adjacent_2, 5)
print(f"task 2: {count_occupied(solved_2)}")

