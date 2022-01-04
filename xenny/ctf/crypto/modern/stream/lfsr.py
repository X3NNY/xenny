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

mask = 0b10100100000010000000100010010100
c = '00100000111111011110111011111000101001001100100111110100000010000011111100110011000111011010100000100011100010101110010111101101000010000011110111110000110010110000111001111010100000110011010101010110100101100011010001011101111101000100110101111100000110000110110000011111010001011001101111001110000100110101111100011101101101101100011101100111011101011101010111011100101110101011011110100111100000111110010010001010001000000011110000011001110010100010010111000010001011110110000010101110011000101011001101111101111010001110010000000101011110001110001110100111011110000111111010110100001010010111001100001101100101011100100111100001100101000100001010001000111010110011111000101110011101000111110110000010000101101010010001111000010101010000011110100001001101111011010000010011110011010110100100001100'
print(mask_attack(mask, c))
# def b_m_attack():