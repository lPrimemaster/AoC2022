def get_priority(item: str):
    if ord(item) >= ord('a'):
        return ord(item) - ord('a') + 1
    else:
        return ord(item) - ord('A') + 27

def load_items(contents: str):
    comp0 = {}
    comp1 = {}
    total = 0

    for item in contents[:len(contents)//2]:
        if item in comp0:
            comp0[item] += 1
        else:
            comp0[item] = 1

    for item in contents[len(contents)//2:]:
        if item in comp1:
            comp1[item] += 1
        else:
            comp1[item] = 1
    
    pkeys = []
    keys = comp0.keys()
    for k, v in comp1.items():
        if k in keys and k not in pkeys:
            total += get_priority(k)
            pkeys.append(k)
    
    return total

def check_group_badge(group: list):
    common = [get_priority(item) for item in group[0] if item in group[1] and item in group[2] and item != "\n"]
    return common[0]
    # print(common)

with open('day3.txt') as f:
    lines = f.readlines()
    total_sum_prio = sum(load_items(l) for l in lines)
    sum_groups = sum(check_group_badge(lines[i:i+3]) for i in range(0, len(lines), 3))

print(total_sum_prio)

print(sum_groups)
