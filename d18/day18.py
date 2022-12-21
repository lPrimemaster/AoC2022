from typing import List
from collections import deque

def neighbours(cube):
    return [
        [cube[0] + 1, cube[1], cube[2]],
        [cube[0] - 1, cube[1], cube[2]],
        [cube[0], cube[1] + 1, cube[2]],
        [cube[0], cube[1] - 1, cube[2]],
        [cube[0], cube[1], cube[2] + 1],
        [cube[0], cube[1], cube[2] - 1]
    ]

def bfs(graph: List[List[int]], cstart, xlims, ylims, zlims):
    out_faces = 0
    
    for cube_face in neighbours(cstart):
        if cube_face in graph: continue
        queue = deque([cube_face])
        visited = [cube_face]
        while queue:
            cube = queue.popleft()
            
            # Original cube sees the outside
            if (cube[0] == (xlims[0] - 1) or cube[0] == (xlims[1] + 1) or
            cube[1] == (ylims[0] - 1) or cube[1] == (ylims[1] + 1) or
            cube[2] == (zlims[0] - 1) or cube[2] == (zlims[1] + 1)):
                out_faces += 1
                break
            
            # This one is not outside
            for ncube in neighbours(cube):
                if ncube in graph: continue
                
                if ncube not in visited:
                    visited.append(ncube)
                    queue.append(ncube)
    return out_faces

with open('day18.txt') as f:
    cubes = [[int(c) for c in l.strip().split(',')] for l in f.readlines()]
    
    # Part 1
    sarea = 0
    for cube in cubes:
        for i in range(3):
            nc = cube.copy()
            nc[i] += 1
            if nc not in cubes:
                sarea += 1
            nc[i] -= 2
            if nc not in cubes:
                sarea += 1
    print('Total surface area:', sarea)
    
    # Part 2 - Use bfs [slow] (dfs could be better ?)
    max_x = max((cube[0] for cube in cubes))
    min_x = min((cube[0] for cube in cubes))
    
    max_y = max((cube[1] for cube in cubes))
    min_y = min((cube[1] for cube in cubes))
    
    max_z = max((cube[2] for cube in cubes))
    min_z = min((cube[2] for cube in cubes))
    
    faces = []
    for i, c in enumerate(cubes):
        print(f'{i}/{len(cubes)}')
        faces.append(bfs(cubes, c, (min_x, max_x), (min_y, max_y), (min_z, max_z)))
    print('Exterior surface area:', sum(faces))
    