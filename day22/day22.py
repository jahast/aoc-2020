import itertools
from typing import List

with open("input.txt", "r") as f:
    raw = [s.strip() for s in f.readlines()]

player_one = [l for l in itertools.takewhile(lambda x: x != "", raw)]

player_two = raw[len(player_one) + 1:]

def prepare(hand):
    wo_first_row = hand[1:]
    return [int(c) for c in wo_first_row]

p1, p2 = prepare(player_one), prepare(player_two)

while len(p1) > 0 and len(p2) > 0:
    p1_c, p2_c = p1.pop(0), p2.pop(0)
    p1, p2 = (p1, [*p2, *[p2_c, p1_c]]) if p2_c > p1_c else ([*p1, *[p1_c, p2_c]], p2)

winning_hand = p1 if len(p1) > len(p2) else p2
ans1 = sum([(i + 1)*n for i, n in enumerate(winning_hand[::-1])])

print(ans1)

P1_WIN = 0
P2_WIN = 1

p1, p2 = prepare(player_one), prepare(player_two)

def subgame(p1: List[int], p2: List[int], i = 0):
    seen = []
    while len(p1) > 0 and len(p2) > 0:
        if (p1,p2) in seen:
            return P1_WIN, []
        seen.append((p1.copy(),p2.copy()))

        p1_c, p2_c = p1.pop(0), p2.pop(0)

        if p1_c <= len(p1) and p2_c <= len(p2):
            winner, _ = subgame(p1[0:p1_c], p2[0:p2_c], i + 1)
        else:
            winner = P1_WIN if p1_c > p2_c else P2_WIN 
        
        p1, p2 = (p1, [*p2, *[p2_c, p1_c]]) if winner == P2_WIN else ([*p1, *[p1_c, p2_c]], p2)
        # print(f"{i}: p1: {p1}, p2: {p2}")

    return (P2_WIN, p2) if len(p1) == 0 else (P1_WIN, p1)

_, hand = subgame(p1, p2)

ans2 = sum([(i + 1)*n for i, n in enumerate(hand[::-1])])
print(ans2)