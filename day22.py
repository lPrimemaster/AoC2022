import numpy as np
import re
import sys

def inc_pos(pos, heading):
    if heading == 0: return [pos[0] + 1, pos[1]]
    if heading == 1: return [pos[0], pos[1] + 1]
    if heading == 2: return [pos[0] - 1, pos[1]]
    if heading == 3: return [pos[0], pos[1] - 1]

def rotate(heading, rot):
    if rot == 'R': return (heading + 1) % 4
    if rot == 'L': return (heading - 1) % 4
    return heading # Handle last step's no turn

# We could make this work for any cube projection
# But lets keep it simple and calculate for the input specific projection only
# Convention (1 -> front, 4 -> back):
# 0
# 1 - 3 4 5
# 2
def get_sextant(pos):
    sx, sy = pos[0] // 50, pos[1] // 50
    if sx == 0:
        if sy == 2: return 3
        elif sy == 3: return 4
    elif sx == 1:
        return sy
    elif sx == 2 and sy == 0: return 5
    return None

def get_next_sextant_pos_heading(sextants, heading):
    sextants[0]

def check_head_pos(board, npos, heading, part):
    if part == 1:
        if heading == 0:
            wall = np.where(board[npos[1]] == 2)[0]
            next1 = np.where(board[npos[1]] == 1)[0][0]
            if len(wall):
                if next1 < wall[0]:
                    npos[0] = next1
                    return npos
                npos[0] = wall[0]
                return npos
            npos[0] = next1
            return npos
        elif heading == 2:
            wall = np.where(board[npos[1]] == 2)[0]
            next1 = np.where(board[npos[1]] == 1)[0][-1]
            if len(wall):
                if next1 > wall[-1]:
                    npos[0] = next1
                    return npos
                npos[0] = wall[-1]
                return npos
            npos[0] = next1
            return npos
        elif heading == 1:
            wall = np.where(board[:, npos[0]] == 2)[0]
            next1 = np.where(board[:, npos[0]] == 1)[0][0]
            if len(wall):
                if next1 < wall[0]:
                    npos[1] = next1
                    return npos
                npos[1] = wall[0]
                return npos
            npos[1] = next1
            return npos
        elif heading == 3:
            wall = np.where(board[:, npos[0]] == 2)[0]
            next1 = np.where(board[:, npos[0]] == 1)[0][-1]
            if len(wall):
                if next1 > wall[-1]:
                    npos[1] = next1
                    return npos
                npos[1] = wall[-1]
                return npos
            npos[1] = next1
            return npos
    elif part == 2:
        return

def char_from_heading(heading):
    if heading == 0: return '>'
    if heading == 1: return 'v'
    if heading == 2: return '<'
    if heading == 3: return '^'

def walk(board, instruction, loc, part=1, dboard=None):
    heading = loc[1]
    pos = loc[0]
    i = 0
    while i < instruction[0]:
        npos = inc_pos(pos, heading)
        npos = [c % s for c, s in zip(npos, board.shape[::-1])]

        if board[npos[1], npos[0]] == 0:
            npos = check_head_pos(board, npos, heading, part)

        if board[npos[1], npos[0]] == 2:
            if dboard is not None:
                dboard[pos[1], pos[0]] = char_from_heading(rotate(heading, instruction[1]))
            return (pos, rotate(heading, instruction[1]))
        
        if dboard is not None:
            dboard[npos[1], npos[0]] = char_from_heading(heading)

        pos = npos
        i += 1
    
    if dboard is not None:
        dboard[pos[1], pos[0]] = char_from_heading(rotate(heading, instruction[1]))
    return pos, rotate(heading, instruction[1])
    

with open('day22.txt') as f:
    puzzle, instructions = f.read().split('\n\n')

    # Parse the puzzle
    cols = puzzle.split('\n')
    max_x = max((len(l) for l in cols))
    max_y = len(cols)

    # This method is pretty but is not the most efficient for wrapping
    board = np.zeros((max_y, max_x), dtype=object)
    dboard = np.zeros((max_y, max_x), dtype=object)
    dboard.fill(' ')

    for y in range(max_y):
        for x in range(len(cols[y])):
            if cols[y][x] == '.':
                dboard[y, x] = '.'
                board[y, x] = 1
            elif cols[y][x] == '#':
                dboard[y, x] = '#'
                board[y, x] = 2
    
    # print(calculate_sextants_bounds(board))

    # Parse the instructions
    steps = [int(s) for s in re.compile('\d+').findall(instructions.strip())]
    turns = re.compile('L|R').findall(instructions.strip())
    turns.append('N')
    instructions = [t for t in zip(steps, turns)]
    start = [np.where(board[0] == 1)[0][0], 0]
    loc = (start, 0)
    for i in instructions:
        loc = walk(board, i, loc, dboard=dboard)
        # np.savetxt('dboard.txt', dboard, fmt='%s')
        # input()
    print('Password:', (loc[0][1]+1)*1000 + (loc[0][0]+1)*4 + loc[1])