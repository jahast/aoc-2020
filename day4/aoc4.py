import string

with open("aoc4.txt", "r") as f:
    raw = f.readlines()

passports = [{}]

for line in raw:
    cleaned = line.strip()

    if line == "\n":
        passports.append({})
        continue
        
    current = passports[-1]
    kvps = cleaned.split(" ")
    for kvp in kvps:
        key, value = kvp.split(":")
        current[key] = value

required_keys = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"]
required_keys_set = set(required_keys)

valids = 0
for passport in passports:
    if required_keys_set.issubset(passport.keys()):

        byr = int(passport["byr"])
        byr_rule = byr >= 1920 and byr <= 2002

        iyr = int(passport["iyr"])
        iyr_rule = iyr >= 2010 and iyr <= 2020

        eyr = int(passport["eyr"])
        eyr_rule = eyr >= 2020 and eyr <= 2030

        hgt = passport["hgt"]
        unit = hgt[-2:]

        if unit not in ["cm", "in"]:
            continue

        height = int(hgt[:-2])
        
        hgt_rule = (unit == "cm" and height >= 150 and height <= 193) or (unit == "in" and height >= 59 and height <= 76)

        hcl: str = passport["hcl"]
        valid_characters = list(string.ascii_lowercase[:6]) + [str(i) for i in range(0,10)]
        hcl_rule = hcl.startswith("#") and len(hcl) == 7 and all([c in valid_characters for c in hcl[1:]])

        ecl: str = passport["ecl"]
        ecl_rule = ecl in ["amb","blu","brn","gry","grn","hzl","oth"]

        pid: str = passport["pid"]
        numbers = [str(i) for i in range(0,10)]
        pid_rule = len(pid) == 9 and all([i in numbers for i in pid])

        if byr_rule and iyr_rule and eyr_rule and hgt_rule and hcl_rule and ecl_rule and pid_rule:
            valids = valids + 1 

print(valids)