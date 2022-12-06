def overlap_fully(inval: list):
    in_range0 = inval[0].split("-")
    in_range1 = inval[1].split("-")

    a0 = int(in_range0[0])
    b0 = int(in_range0[1])

    a1 = int(in_range1[0])
    b1 = int(in_range1[1])

    r0 = range(a0, b0 + 1)
    r1 = range(a1, b1 + 1)

    if a0 in r1 and b0 in r1:
        return 1
    
    if a1 in r0 and b1 in r0:
        return 1
    
    return 0

def overlap(inval: list):
    in_range0 = inval[0].split("-")
    in_range1 = inval[1].split("-")

    a0 = int(in_range0[0])
    b0 = int(in_range0[1])

    a1 = int(in_range1[0])
    b1 = int(in_range1[1])

    r0 = range(a0, b0 + 1)
    r1 = range(a1, b1 + 1)

    if a0 in r1 or b0 in r1:
        return 1
    
    if a1 in r0 or b1 in r0:
        return 1
    
    return 0

with open('day4.txt') as f:
    print(sum([overlap(l.split(",")) for l in f.readlines()]))