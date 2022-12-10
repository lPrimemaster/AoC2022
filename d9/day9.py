import numpy as np
import pprint as pp
import copy
import time

def move_tail(head, tail):
    diff = head - tail
    sign_diff = np.sign(diff)
    if np.linalg.norm(diff) >= 2.0:
        tail[0] += sign_diff[0]
        tail[1] += sign_diff[1]
    
    return tail

def move_head(instruction, head):
    if instruction.startswith('U'):
        return head + [0,  1]
    if instruction.startswith('D'):
        return head + [0, -1]
    if instruction.startswith('L'):
        return head + [-1, 0]
    if instruction.startswith('R'):
        return head + [ 1, 0]
    
def same(i, j, arr):
    return arr[0] == i and arr[1] == j
    
def print_frame(n, head_path, tail_path, size):
    print(knots_path[n])
    for i in range(-size, size):
        for j in range(-size, size):
            pn = False
            if same(i, j, head_path[n]):
                print('H', end='')
                continue
            
            for knot_n, knot in enumerate(knots_path[n]):
                if same(i, j, knot):
                    print(f'{knot_n}', end='')
                    pn = True
                    break
            
            if not pn:
                if same(i, j, tail_path[n]):
                    print('T', end='')
                else:
                    print('.', end='')
        
        print('\n', end='')
        
    diff = head_path[n] - tail_path[n]
    distance = np.linalg.norm(diff)
    print(diff, distance)
    print('')
    
    
N = 8
head = np.array([0, 0])
knots = [np.zeros(2) for _ in range(N)]
tail = np.array([0, 0])

head_path = [head.copy()]
knots_path = [copy.deepcopy(knots)]
tail_path = [tail.copy()]


with open('day9.txt') as f:
    instructions = f.readlines()
    
    for i in instructions:
        for _ in range(int(i.split()[1])):
            head = move_head(i, head)
            knots[0] = move_tail(head, knots[0])
            for n in range(1, N):
                knots[n] = move_tail(knots[n-1], knots[n])
            tail = move_tail(knots[N-1], tail)
            
            head_path.append(head.copy())
            knots_path.append(copy.deepcopy(knots))
            tail_path.append(tail.copy())
    
    # for i in range(len(tail_path)):
    #     print_frame(i, head_path, tail_path, 10)
    #     time.sleep(0.2)
    
    print(len(set(map(tuple, tail_path))))
    