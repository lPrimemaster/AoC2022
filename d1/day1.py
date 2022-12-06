
with open('day1.txt') as f:
    calories_per_elf = [sum(int(cal) for cal in elf.split("\n")) for elf in f.read().split("\n\n")]

# Elf with the most calories
print(max(calories_per_elf))

# Top three caloric elves sum
print(sum(sorted(calories_per_elf, reverse=True)[:3]))