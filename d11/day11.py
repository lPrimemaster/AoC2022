from typing import List
import math

class Monkey:
    def __init__(self, items, op, test, correspondence) -> None:
        self.items = items
        self.op = op
        self.test = test
        self.correspondence = correspondence
        self.total_inspections = 0
        self.contribution = 0
        
    def add_items(self, items):
        self.items.extend(items)
    
    def remove_items(self, items):
        self.items = list(set(self.items) - set(items))
    
    def __repr__(self) -> str:
        # print('Items: ', self.items)
        print('Inspections: ', self.total_inspections)
        print('Contribution Score: ', self.contribution)
        return ''

# We are lazy, we use eval
def operate_worry_level(monkey: Monkey, monkeys: List[Monkey], factor: int):
    to_remove = []
    for w in monkey.items:
        old = w
        new = eval(monkey.op)
        to_send = monkey.correspondence[1]
        
        # print('Pre: ', len(str(old)))
        
        new %= factor
        
        if new % monkey.test == 0:
            to_send = monkey.correspondence[0]
        # print('Pos: ', len(str(new)))
        # print(old, new, to_send, new % monkey.test)
        monkeys[to_send].add_items([new])
        to_remove.append(old)
        monkey.total_inspections += 1
    monkey.remove_items(to_remove)
    
with open('day11.txt') as f:
    monkeys_str = [m.split('\n') for m in f.read().split('\n\n')]
    monkeys = []
    for monkey in monkeys_str:
        monkeys.append(
            Monkey(
                [int(i) for i in monkey[1].split(':')[1].strip().split(',')],
                monkey[2].split(':')[1].split('=')[1].strip(),
                int(monkey[3].split()[-1].strip()),
                [int(monkey[4].split()[-1].strip()), int(monkey[5].split()[-1].strip())]
            )
        )

    for r in range(10000):
        # if r % 50 == 0:
        print('Round: ', r)
            
        for m in monkeys:
            # print(m)
            operate_worry_level(m, monkeys, math.prod([d.test for d in monkeys]))
    print('\n\n')
    
    for m in monkeys:
        print(m)

    inspections = [m.total_inspections for m in monkeys]
    top_monkeys = sorted(inspections, reverse=True)[:2]
    print('Monkey business: ', top_monkeys[0] * top_monkeys[1])