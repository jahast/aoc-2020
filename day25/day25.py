pkey1 = 3418282
pkey2 = 8719412

def find(pkey):
    i = 0
    val = 1
    while val != pkey:
        val *= 7
        val %= 20201227
        i += 1
    return i

slz1 = find(pkey1)
slz2 = find(pkey2)

ans1 = 1
for i in range(0, slz1):
    ans1 *= pkey2
    ans1 %= 20201227

print(ans1)