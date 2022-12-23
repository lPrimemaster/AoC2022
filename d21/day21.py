from __future__ import annotations
from typing import Dict

class Node:
    def __init__(self, dependencies: str) -> None:
        if dependencies.isdecimal():
            self.v = int(dependencies)
            self.dependencies = []
        else:
            self.v = None
            d = dependencies.strip().split(' ')
            self.dependencies = d[::2]
            self.op = d[1]

    def calc(self, graph: Dict[str, Node]):
        if self.v != None:
            return self.v
        else:
            if self.op == '*':
                return graph[self.dependencies[0]].calc(graph) * graph[self.dependencies[1]].calc(graph)
            elif self.op == '/':
                return graph[self.dependencies[0]].calc(graph) // graph[self.dependencies[1]].calc(graph)
            elif self.op == '+':
                return graph[self.dependencies[0]].calc(graph) + graph[self.dependencies[1]].calc(graph)
            elif self.op == '-':
                return graph[self.dependencies[0]].calc(graph) - graph[self.dependencies[1]].calc(graph)
    
    def depends_on(self, graph: Dict[str, Node], dep: str):
        if self.v: return False
        if self.dependencies[0] == dep or self.dependencies[1] == dep: return True
        if graph[self.dependencies[0]].depends_on(graph, dep): return True
        if graph[self.dependencies[1]].depends_on(graph, dep): return True
        return False

with open('day21.txt') as f:
    # Part 1
    graph = {l.split(':')[0].strip(): Node(l.split(':')[1].strip()) for l in f.readlines()}
    print('Value of root:', graph['root'].calc(graph))

    # Part 2 - A lot of assumptions!!!! But it works!
    # jmsg does not appear to depend on humn (lets assume continuity and linearity on the other end)
    # print(graph['jmsg'].depends_on(graph, 'humn'))

    # Assuming linearity, binary search the value
    # (we could reverse the stack of operations and calculate the value)
    graph['root'].op = '-'
    v = 0
    lv0 = 0
    ns = []
    done = False
    while True:
        graph['humn'].v = sum(ns) + 10**v
        v0 = graph['root'].calc(graph)
        if (v0 > 0 and lv0 < 0) or (v0 < 0 and lv0 > 0): # Sign search
            ns.append(10 ** (v - 1))
            v = 0
        if abs(v0) < 100: # Linear search for low value of v
            v = 0
            while True:
                graph['humn'].v = sum(ns) + v
                v0 = graph['root'].calc(graph)
                if v0 == 0:
                    print('Value to yell:', sum(ns) + v)
                    done = True
                    break
                v += 1 # Assuming monotonic increasing
        if done:
            break
        lv0 = v0
        v += 1