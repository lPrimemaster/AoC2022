import re

def distance_from_sensor(pos, sensor):
    return abs(pos[0] - sensor[0]) + abs(pos[1] - sensor[1])

def tuning_frequency(pos):
    return pos[0] * 4000000 + pos[1]


with open('day15.txt') as f:
    lines = f.readlines()
    
    find_integer = re.compile('-?\d+')
    sensors = []
    sensors_distance = []
    
    for line in lines:
        sx, sy, bx, by = find_integer.findall(line)
        sensors.append((int(sx), int(sy)))
        sensors_distance.append(distance_from_sensor((int(bx), int(by)), sensors[-1]))
    
    target_row = 2000000
    
    total_span = []
    for i in range(len(sensors)):
        span = sensors_distance[i] - abs(target_row - sensors[i][1])
        if span >= 0:
            bounds = [sensors[i][0] - span, sensors[i][0] + span]
            total_span.extend([i for i in range(bounds[0], bounds[1] + 1)]) # Just a hack instead of check for bounds, but slow
            # print(abs(target_row - sensors[i][1]) / sensors_distance[i], sensors_distance[i], span)
    
    positions = list(set(total_span)) # Just a hack instead of check for bounds, but slow
    
    # There is one beacon at the row 2000000 -> so -1 (hackish, but the file is small and works)
    print('Tiles not possible to be in:', len(positions) - 1)
    
    # Part 2 - Using bounds, the method above is slow (No wonder!)
    
    N = 4000000
    for target_row in range(N + 1):
        
        if target_row % 1000 == 0:
            print(f'Checking row {target_row}/{N}')
        
        all_bounds = []
        for i in range(len(sensors)):
            span = sensors_distance[i] - abs(target_row - sensors[i][1])
            if span >= 0:
                bx = sensors[i][0] - span
                by = sensors[i][0] + span
                
                bx = bx if bx > 0 else 0
                bx = bx if bx < N else N
                by = by if by > 0 else 0
                by = by if by < N else N
                
                bounds = (bx, by)
                all_bounds.append(bounds)
                # print(abs(target_row - sensors[i][1]) / sensors_distance[i], sensors_distance[i], span)
        
        all_bounds = sorted(all_bounds, key=lambda x: x[0]) # Sort bounds by xmin
        gap_found = False
        gap_x = 0
        max_x_bound = -1 # x lower limited to 0
        for i in range(len(all_bounds) - 1):
            max_x_bound = max(max_x_bound, all_bounds[i][1])
            if max_x_bound < all_bounds[i+1][0]:
                # Found a gap
                gap_found = True
                gap_x = all_bounds[i+1][0] - 1 # Assume there is only one slot
                break
            
        
        if gap_found:
            pos = (gap_x, target_row)
            print('Found location:', pos)
            print('Tuning frequency:', tuning_frequency(pos))
            break
            
        
    
       