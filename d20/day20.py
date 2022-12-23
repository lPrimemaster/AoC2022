with open('day20.txt') as f:
    # For part 1 replace DK = 1, T = 1
    DK = 811589153
    T = 10
    l = [int(v) * DK for v in f.readlines()]
    o = [i for i in range(len(l))]

    t = 0
    while t < T:
        i = 0
        while i < len(l):
            p = o.index(i)
            np = (p + l[i]) % (len(l) - 1)
            if np == 0 and np < p: np = len(l)
            o.insert(np, o.pop(o.index(i)))
            i += 1
        t += 1

    l = [l[v] for v in o]
    coords = [l[(l.index(0) + offset) % len(l)] for offset in [1000, 2000, 3000]]
    print(coords)
    print(sum(coords))
