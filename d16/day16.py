from __future__ import annotations
from typing import List, Dict, Tuple
from collections import deque
import math
import re
import pprint as pp

class Valve:
    def __init__(self, name, rate, neighbours) -> None:
        self.name = name
        self.neighbours = neighbours
        self.rate = rate
    def __repr__(self) -> str:
        return self.name + ' | ' + str(self.rate) + ' | ' + ','.join(self.neighbours)
        

def make_graph(lines: List[str]) -> Dict[str, Valve]:
    r = re.compile('[A-Z]\w+|\d+')
    valves = {}
    # Read all valves
    for line in lines:
        array = r.findall(line)
        valves[array[1]] = Valve(array[1], int(array[2]), array[3:])
    return valves

def floyd_warshall(graph: Dict[str, Valve]):
    w = {
        x: {y: 1 if y in graph[x].neighbours else math.inf for y in graph.keys()} for x in graph.keys()
    }
    for x in graph.keys():
        w[x][x] = 0
    
    for k in w:
        for i in w:
            for j in w:
                sw = w[i][k] + w[k][j]
                if w[i][j] > sw:
                    w[i][j] = sw
    return w

def bfs(graph: Dict[str, Valve], w: Dict[str, Dict[str, float]], start: str = 'AA', time: int = 30):
    # Queue item = (valve currently at, time left, total flow at the end, visited valves)
    queue = deque([(graph[start], time, 0, [])])
    path_flow = {}
    
    valves_with_rate = [x for x in graph.values() if x.rate > 0] # Ignore final targets with flow rate 0
    
    while queue:
        v, t, f, vv = queue.popleft()
        # print('Time left:', t, '| Paths lenght:', len(vv))
        path_flow['-'.join(vv)] = f
        
        for u in valves_with_rate:
            new_t = t - w[v.name][u.name] - 1 # Minus one, the time to activate the valve
            if new_t <= 0: continue # No negative times allowed
            
            # Ignore previously visited paths
            if u.name not in vv:
                cvv = vv.copy()
                cvv.append(u.name)
                queue.append((u, new_t, f + new_t*u.rate, cvv))
    return path_flow

with open('day16.txt') as f:
    # Common
    valves = make_graph(f.readlines())
    weights = floyd_warshall(valves)
    
    # Part 1
    paths = bfs(valves, weights)
    print('Max flow:', max(flow for flow in paths.values()))
    
    # Part 2
    paths = bfs(valves, weights, time=26)
    total_max = 0
    best_k = []
    it = 0
    total_p = len(paths.keys())**2
    
    for k1, v1 in paths.items():
        for k2, v2 in paths.items():
            it += 1
            valves1 = k1.split('-')
            valves2 = k2.split('-')
            if not set(valves1).intersection(valves2):
                local_flow = v1 + v2
                if total_max <= local_flow:
                    total_max = local_flow
                    best_k = [k1, k2]
            if it % 10000 == 0:
                print(f'Done: {(it/total_p)*100:.6f}%', 'Best Candidate:', best_k)
            
    print('Max flow:', total_max)
    print('Path:', best_k)
    