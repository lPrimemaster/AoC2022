import numpy as np

cycle = []

with open('day10.txt') as f:
    instructions = f.readlines()
    X = 1
    for inst in instructions:
        if inst.startswith('noop'):
            cycle.append(X)
        elif inst.startswith('addx'):
            cycle.append(X)
            cycle.append(X)
            X += int(inst.split()[1])

indices = [20 + 40 * i - 1 for i in range(6)]
weights = [20 + 40 * i for i in range(6)]

# Get the cycles score
print(np.take(cycle, indices))
score = np.multiply(np.take(cycle, indices), weights)
print(np.sum(score))

def px_overlap(cycle, pos, width):
    return cycle[pos] == (pos % width) or cycle[pos] + 1 == (pos % width) or cycle[pos] - 1 == (pos % width)

for j in range(6):
    for i in range(40):
        pos = i + j * 40
        # print(pos)
        if px_overlap(cycle, pos, 40):
            print('#', end='')
        else:
            print('.', end='')
    print('')
