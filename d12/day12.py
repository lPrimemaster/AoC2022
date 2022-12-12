import numpy as np
from typing import Tuple, Optional
from collections import deque
import math

Location = Tuple[int, int]
    
def neighbours(array, i, j):
    ret_neighbours = []
    if i > 0:
        ret_neighbours.append((i-1, j))
    if i < array.shape[0] - 1:
        ret_neighbours.append((i+1, j))
    if j > 0:
        ret_neighbours.append((i, j-1))
    if j < array.shape[1] - 1:
        ret_neighbours.append((i, j+1))
    return ret_neighbours


def bfs(start: Location, goal: Location, array):
    queue = deque([(start[0], start[1], 0)])
    visited = set()
    
    while queue:
        i, j, d = queue.popleft()
        
        if (i, j) == goal:
            return d
        
        for ni, nj in neighbours(array, i, j):
            if array[ni, nj] - array[i, j] <= 1 and (ni, nj) not in visited:
                visited.add((ni, nj))
                queue.append((ni, nj, d+1))
    
    # Not found
    return 9999999999

with open('day12.txt') as f:
    lines = f.readlines()
    
    height_map = np.array([[h for h in l.strip()] for l in lines])
    
    start_i, start_j = np.where(height_map == 'S')
    end_i, end_j = np.where(height_map == 'E')
    print('Start: ', start_i[0], start_j[0])
    print('End:   ', end_i[0], end_j[0])
    
    height_map[start_i[0], start_j[0]] = 'a'
    height_map[end_i[0], end_j[0]] = 'z'
    
    multiple_start = np.where(height_map == 'a')
    
    height_map = np.array([[ord(h) - ord('a') for h in line] for line in height_map])
    
    print(bfs((start_i[0], start_j[0]), (end_i[0], end_j[0]), height_map))
    
    many_starts = [bfs((multiple_start[0][sidx], multiple_start[1][sidx]), (end_i[0], end_j[0]), height_map) for sidx in range(len(multiple_start[0]))]
    
    print(min(many_starts))
    
    