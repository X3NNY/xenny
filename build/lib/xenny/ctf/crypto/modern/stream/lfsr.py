def mask_attack(mask, c):
    li = []
    for i in range(32):
        temp = '1' + ''.join(li) + c[:31-len(li)]
        res = 0
        for j in range(32):
            if mask & (1 << j):
                res ^= int(temp[31-j])
        if res == int(c[31-len(li)]):
            li.insert(0, '1')
        else:
            li.insert(0, '0')
    return hex(int(''.join(li), 2))
