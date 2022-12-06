import re

#001 005 009 013 017 ...
#[P] [H] [P] [Q] [P] [M] [P] [F] [D]
# 1   2   3   4   5   6   7   8   9 
# an = 1 + (n-1)*4 => n = (an - 1) / 4 + 1

def pos_to_n(pos: int):
    return (pos - 1) // 4 + 1

def move(stack, ammount: int, start: int, end: int):
    for _ in range(ammount):
        stack[end-1].append(stack[start-1][-1])
        del stack[start-1][-1]

def move_n(stack, ammount: int, start: int, end: int):
    stack[end-1].extend(stack[start-1][-ammount:])
    del stack[start-1][-ammount:]

def top(stack):
    for s in stack:
        print(s[-1], end='')
    print('\n', end='')

with open('day5.txt') as f:
    file = f.read().split("\n\n")
    hstacks = file[0].split("\n")

    stack = [[] for _ in range(9)]

    r = re.compile("[A-Z]")
    for hs in hstacks:
        for match in r.finditer(hs):
            index = pos_to_n(match.start()) - 1
            stack[index].append(match.group())
    
    for i in range(len(stack)):
        stack[i] = stack[i][::-1]

    instructions = file[1].split("\n")

    for inst in instructions:
        args = [int(n) for n in re.findall("[0-9]+", inst)]
        # move(stack, *args)
        move_n(stack, *args)

    top(stack)
