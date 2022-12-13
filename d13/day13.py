def check_order(v1, v2):
    i = 0
    
    while i < min(len(v1), len(v2)):
        v1list = isinstance(v1[i], list)
        v2list = isinstance(v2[i], list)
        anylist = v1list or v2list
        ordered = True
        
        if not anylist:
            if v1[i] > v2[i]:
                return False, False
            elif v1[i] < v2[i]:
                return True, True
            i += 1
            continue
        
        if v1list and v2list:
            ordered, done = check_order(v1[i], v2[i])
        elif v1list:
            ordered, done = check_order(v1[i], [v2[i]])
        elif v2list:
            ordered, done = check_order([v1[i]], v2[i])
        
        if done:
            return ordered, True
        
        if not ordered:
            return False, False
        
        i += 1
    
    if len(v1) == len(v2):
        return len(v1) <= len(v2), False
    return len(v1) < len(v2), True

# Why not, just wtv, the array is not that large
def buble_sort(array):
    n = len(array)
    swapped = False
    for i in range(n-1):
        for j in range(0, n-i-1):
            ordered, _ = check_order(array[j + 1], array[j])
            if ordered:
                swapped = True
                array[j], array[j + 1] = array[j + 1], array[j]
         
        if not swapped:
            return

with open('day13.txt') as f:
    pairs = []
    for p in f.read().split('\n\n'):
        pairs.append([eval(packet) for packet in p.split('\n')])
    
    packet_index = 1
    total_sum = 0
    all_packets = [[[2]], [[6]]]
    for v0, v1 in pairs:
        all_packets.append(v0)
        all_packets.append(v1)
        ordered, _ = check_order(v0, v1)
        if ordered:
            print('\033[32m Packet ordered. \033[39m')
            total_sum += packet_index
        else:
            print('\033[31m Packet not ordered. \033[39m')
            
        # if packet_index == 1:    
        #     break
        packet_index += 1
        
    print('Total ordered packets index sum: ', total_sum)
    
    buble_sort(all_packets)
    
    divider_indices = []
    for i, p in enumerate(all_packets):
        if p == [[2]] or p == [[6]]:
            divider_indices.append(i+1)
            
    print('Divider indices product: ', divider_indices[0] * divider_indices[1])
    