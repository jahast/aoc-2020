with open("aoc12.txt", "r") as f:
    raw = f.readlines()

directions = ["E", "S", "W", "N"]
turns = ["L", "R"]

def apply_direction_delta(old, delta):
    return (old[0] + delta[0], old[1] + delta[1])

def map_direction(direction, quantity):
    if direction == "E":
        return (quantity, 0)
    elif direction == "W":
        return (-quantity, 0)
    elif direction == "N":
        return (0, quantity)
    elif direction == "S":
        return (0, -quantity)


def map_to_new_direction(old, left_or_right, quantity):
    n_dirs = quantity // 90
    old_index = directions.index(old)
    index_delta = n_dirs if left_or_right == "R" else -n_dirs
    new_index = (old_index + index_delta) % len(directions)
    return directions[new_index]


def map_rotation_to_location(old_location, left_or_right, quantity):
    n_dirs = quantity // 90
    r_turn = lambda x: (x[1], -x[0])
    l_turn = lambda x: (-x[1], x[0])

    transformer = r_turn if left_or_right == "R" else l_turn
    new = tuple(old_location)

    for _ in range(0,n_dirs):
        new = transformer(new)

    return new


# task 1
location = (0,0)
current_direction = "E"

for line in raw:
    instruction = line[0]
    quantity = int(line[1:])

    if instruction in directions:
        delta = map_direction(instruction, quantity)
        location = apply_direction_delta(location, delta)
        continue
    
    if instruction == "F":
        delta = map_direction(current_direction, quantity)
        location = apply_direction_delta(location, delta)
        continue
    
    if instruction in turns:
        new_direction = map_to_new_direction(current_direction, instruction, quantity)
        current_direction = new_direction
        continue

    raise Exception()

print(abs(location[0]) + abs(location[1]))

# task 2
ship_location = (0,0)
waypoint_location = (10, 1)

for line in raw:
    instruction = line[0]
    quantity = int(line[1:])

    if instruction in directions:
        delta = map_direction(instruction, quantity)
        waypoint_location = apply_direction_delta(waypoint_location, delta)
        continue
    
    if instruction == "F":
        delta = (waypoint_location[0] * quantity, waypoint_location[1] * quantity)
        ship_location = apply_direction_delta(ship_location, delta)
        continue

    if instruction in turns:
        waypoint_location = map_rotation_to_location(waypoint_location, instruction, quantity)
        continue

    raise Exception()

print(f"ship location: {ship_location}, waypoint location: {waypoint_location}")
print(abs(ship_location[0]) + abs(ship_location[1]))