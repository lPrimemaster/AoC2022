from __future__ import annotations
from typing import List, Tuple
import numpy as np

class AABB:
    def __init__(self, x, y, w, h) -> None:
        self.x0 = x
        self.x1 = x + w - 1
        
        self.y0 = y
        self.y1 = y + h - 1
        
        self.w = w
        self.h = h
        
    def isect(self, other: AABB) -> bool:
        return self.x0 <= other.x1 and self.x1 >= other.x0 and self.y0 <= other.y1 and self.y1 >= other.y0
    
    def move(self, x, y):
        self.x0 += x
        self.x1 += x
        self.y0 += y
        self.y1 += y
        
    def minX(self): return self.x0
    def minY(self): return self.y0
    def maxX(self): return self.x1
    def maxY(self): return self.y1
    
class Rock:
    def __init__(self, t, y0) -> None:
        self.t = t
        
        if t == 0: 
            self.bounds = [AABB(2, y0, 4, 1)]
            self.qbound = AABB(2, y0, 4, 1)
        elif t == 1: 
            self.bounds = [AABB(3, y0, 1, 1), AABB(2, y0 + 1, 3, 1), AABB(3, y0 + 2, 1, 1)]
            self.qbound = AABB(2, y0, 3, 3)
        elif t == 2: 
            self.bounds = [AABB(2, y0, 3, 1), AABB(4, y0 + 1, 1, 2)]
            self.qbound = AABB(2, y0, 3, 3)
        elif t == 3: 
            self.bounds = [AABB(2, y0, 1, 4)]
            self.qbound = AABB(2, y0, 1, 4)
        else:        
            self.bounds = [AABB(2, y0, 2, 2)]
            self.qbound = AABB(2, y0, 2, 2)
        
    def isect(self, other: Rock):
        for b0 in self.bounds:
            for b1 in other.bounds:
                if b0.isect(b1):
                    return True
        return False
    
    def move(self, x, y):
        for b in self.bounds:
            b.move(x, y)
        self.qbound.move(x, y)
    
def jet_and_fall(r: Rock, j: str, rocks: List[Rock]) -> Tuple[bool, int]:
    # print_frame(rocks, r)
    # Jet left
    if j == '<' and r.qbound.minX() > 0:
        r.move(-1, 0)
    # Jet right
    elif j == '>' and r.qbound.maxX() < 6:
        r.move(1, 0)
        
    # Check for other rocks
    for rock in rocks[::-1]:
        if r.isect(rock):
            if j == '<':
                r.move(1, 0)
                break
            if j == '>':
                r.move(-1, 0)
                break
    
    # Fall
    r.move(0, -1)
    
    # Hit the ground
    if r.qbound.minY() < 0:
        r.move(0, 1)
        rocks.append(r)
        if len(rocks) > 50: rocks.pop(0) # Keep only the last 50 rocks in the stack
        return True, r.qbound.maxY() + 1
    
    # Check for other rocks
    for rock in rocks[::-1]:
        if r.isect(rock):
            r.move(0, 1)
            rocks.append(r)
            if len(rocks) > 50: rocks.pop(0) # Keep only the last 50 rocks in the stack
            return True, r.qbound.maxY() + 1
        
    return False, r.qbound.maxY() + 1
    
with open('day17.txt') as f:
    moves = f.read()
    lmoves = len(moves)
    stopped_rocks = []
    rock_type = 0
    i = 0
    j = 0
    ymax = 0
    
    print('Calculating part1...')
    while i < 2022:
        rock_type = i % 5
        rock = Rock(rock_type, ymax + 3)
        stopped = False
        while not stopped:
            stopped, y = jet_and_fall(rock, moves[j % lmoves], stopped_rocks)
            j += 1
        ymax = max(ymax, y)
        i += 1
    print('Stopped rocks:', i, 'ymax:', ymax)
        
    # Part 2
    stopped_rocks = []
    rock_type = 0
    i = 0
    j = 0
    ymax = 0
    pattern_found = False
    
    jets = []
    jj = 0
    jmatch = False
    ly = 0
    li = 0
    
    R = 1000000000000
    
    print('Calculating part2...')
    while not pattern_found:
        rock_type = i % 5
        rock = Rock(rock_type, ymax + 3)
        stopped = False
        while not stopped:
            stopped, y = jet_and_fall(rock, moves[j % lmoves], stopped_rocks)
            j += 1
        ymax = max(ymax, y)
        i += 1
        
        if rock_type == 0:
            jetmove = (j % lmoves)
            
            if jetmove == 5 and not jmatch:
                jets.clear()
                jj = 0
                jmatch = True
                
            if jets and jetmove == jets[jj]:
                jj += 1
                if jj == len(jets):
                    print('Found sequence! Total rocks until now:', li)
                    print(f'Stopped rocks diff: {(i-li):9d} ymax diff: {(ymax - ly):9d}')
                    
                    if li > 0:
                        print(f'Estimated height at {R} rocks:', ly + int(np.ceil((R - li) / (i-li) * (ymax - ly))))
                        pattern_found = True
                        break
                    li = i
                    ly = ymax
                    jj = 0
            else:
                jets.append(jetmove)
                jj = 0
