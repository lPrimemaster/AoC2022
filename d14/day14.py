import numpy as np
from scipy.interpolate import interp1d
import copy

def simulate(cave, start):
    # Simulate one grain at a time until it stops, or falls
    
    place_pos = np.where(np.logical_or(cave[:, start[0]] == 1, cave[:, start[0]] == 2))[0][0] - 1
    
    # The sand is blocked
    if place_pos == start[1] and cave[place_pos + 1, start[0] - 1] != 0 and cave[place_pos + 1, start[0] + 1] != 0:
        cave[place_pos, start[0]] = 2
        return False
    
    # Check if the left diag slot is free
    x = start[0]
    y = place_pos
    while True:
        
        if y + 1 >= cave.shape[0]:
            return False
        if x + 1 >= cave.shape[1]:
            return False
        if x - 1 < 0:
            return False
        
        if cave[y + 1, x] == 0:
            y += 1
            continue
        elif cave[y + 1, x - 1] == 0:
            y += 1
            x -= 1
            continue
        elif cave[y + 1, x + 1] == 0:
            y += 1
            x += 1
            continue
        else:
            # Set the sand there
            cave[y, x] = 2
            return True
        
    
    

with open('day14.txt') as f:
    paths = [[[int(v) for v in p.strip().split(',')] for p in l.split(' -> ')] for l in f.readlines()]
    paths2 = copy.deepcopy(paths)
    
    min_x = min(list(map(lambda x: min([point[0] for point in x]), paths)) + [500])
    max_x = max(list(map(lambda x: max([point[0] for point in x]), paths)) + [500])
    
    min_y = min(list(map(lambda x: min([point[1] for point in x]), paths)) + [0])
    max_y = max(list(map(lambda x: max([point[1] for point in x]), paths)) + [0])
    
    linear_transform_x = interp1d([min_x, max_x], [0, max_x-min_x])
    linear_transform_y = interp1d([min_y, max_y], [0, max_y-min_y])
    
    sand_start = [int(linear_transform_x(500)), int(linear_transform_y(0))]
    print('Sand start:', sand_start)
    
    for i, path in enumerate(paths):
        for j, point in enumerate(path):
            paths[i][j][0] = int(linear_transform_x(paths[i][j][0]))
            paths[i][j][1] = int(linear_transform_y(paths[i][j][1]))
            
    cave = np.zeros((max_y-min_y + 1, max_x-min_x + 1))
    
    # Key
    # 0 -> Air
    # 1 -> Wall
    # 2 -> Sand
    
    for path in paths:
        start = path[0]
        for line in np.diff(path, axis=0):
            inc = np.sum(np.sign(line))
            
            i = inc if line[0] != 0 else 0
            j = inc if line[1] != 0 else 0
            
            for x in range(np.abs(np.sum(line))):
                cave[start[1], start[0]] = 1
                start[0] += i
                start[1] += j
            cave[start[1], start[0]] = 1
            
    
    while simulate(cave, sand_start): continue
    
    sand_mask = cave == 2
    print('Units of sand:', sand_mask.sum())
    
    # We could calculate the majorant for the floor x span but, just creating a large enough array should be ok
    # There is also a way to calculate this without the need to simulate I believe
    max_y += 2
    
    min_x -= 1000
    max_x += 1000
    
    linear_transform_x = interp1d([min_x, max_x], [0, max_x-min_x])
    linear_transform_y = interp1d([min_y, max_y], [0, max_y-min_y])
    
    sand_start = [int(linear_transform_x(500)), int(linear_transform_y(0))]
    print('Sand start:', sand_start)
    
    for i, path in enumerate(paths2):
        for j, point in enumerate(path):
            paths2[i][j][0] = int(linear_transform_x(paths2[i][j][0]))
            paths2[i][j][1] = int(linear_transform_y(paths2[i][j][1]))
    
    cave = np.zeros((max_y-min_y + 1, max_x-min_x + 1))
    cave[max_y, :] = 1
    
    print(cave.shape)
    
    for path in paths2:
        start = path[0]
        for line in np.diff(path, axis=0):
            inc = np.sum(np.sign(line))
            
            i = inc if line[0] != 0 else 0
            j = inc if line[1] != 0 else 0
            
            for x in range(np.abs(np.sum(line))):
                cave[start[1], start[0]] = 1
                start[0] += i
                start[1] += j
            cave[start[1], start[0]] = 1
    
    while simulate(cave, sand_start): continue
    
    sand_mask = cave == 2
    print('Units of sand:', sand_mask.sum())
    
    
    
    
    
    