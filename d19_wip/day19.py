import re
from collections import deque
from typing import List
from operator import add

TYPES = ['ore', 'clay', 'obsidian', 'geode']
TORE = 0
TCLAY = 1
TOBSIDIAN = 2
TGEODE = 3

class Blueprint:
    def __init__(self, line: str) -> None:
        ore, clay, oore, oclay, gore, gobsidian = [int(d) for d in re.compile('\d+').findall(line.split(':')[1])]
        self.cost = [ore, clay, (oore, oclay), (gore, gobsidian)]
        self.total_cost = ore + oclay + oore + gore

def dfs(graph):
    pass

def iterate_all(blueprints: List[Blueprint]):
    pass

with open('day19.txt') as f:
    blueprints = [Blueprint(line) for line in f.readlines()]
    
    print(iterate_all(blueprints[:]))
    