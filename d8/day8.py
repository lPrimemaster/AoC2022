import numpy as np

with open('day8.txt') as f:
    N = 99
    trees = np.empty((N, N))
    visible = np.zeros((N, N))
    score = np.zeros((N, N))
    
    visible[N-1, :] = 1
    visible[0, :] = 1
    visible[:, N-1] = 1
    visible[:, 0] = 1
    
    def score_f(trees, size):
        scoreval = 0
        for t in trees:
            scoreval += 1
            if t >= size:
                return scoreval
        return scoreval
    
    
    for i in range(N):
        trees[i] = [int(t) for t in f.readline() if t.isdigit()]
    
    # Check 1-by-1 ?
    for i in range(1, N-1):
        for j in range(1, N-1):
            if visible[i, j] == 1:
                continue
            
            # In a circle until first neighbour in xy plane is found (?)
            size = trees[i, j]
            
            # print(size, trees[i, j:], np.max(trees[i, j:]))
            
            # Calculate visibility
            if size > np.max(trees[i, j+1:]): # Right
                visible[i, j] = 1
            elif size > np.max(trees[i, :j]): # Left
                visible[i, j] = 1
            elif size > np.max(trees[:i, j]): # Up
                visible[i, j] = 1
            elif size > np.max(trees[i+1:, j]): # Down
                visible[i, j] = 1
                
            # Calculate score
            score[i, j] = 1
            score[i, j] *= score_f(trees[i, j+1:], size) # Right
            score[i, j] *= score_f(trees[i, :j][::-1], size) # Left
            score[i, j] *= score_f(trees[:i, j][::-1], size) # Up
            score[i, j] *= score_f(trees[i+1:, j], size) # Down
    
    print(visible)           
    print(np.sum(visible))
    
    print(score)
    print(np.max(score))