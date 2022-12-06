# There is certainly a more efficient way of doing this but, the input is not that large...
def get_marker_end_index(msg: str, marker_size: int) -> int:
    for i in range(0, len(msg)-marker_size):
        d = {}
        failed = False
        print('Checking ', msg[i:i+marker_size])
        for c in msg[i:i+marker_size]:
            if c in d:
                failed = True
                break
            else:
                d[c] = 1
        if not failed:
            return i+marker_size



with open('day6.txt') as f:
    # print(get_marker_end_index(f.read(), 4))
    print(get_marker_end_index(f.read(), 14))
