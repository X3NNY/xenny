def encode(content: bytes, key: int):
    while key < 0:
        key += 26
    p = list(content)
    oa = ord('a')
    oz = ord('z')
    oA = ord('A')
    oZ = ord('Z')
    for i in range(len(p)):
        if oa <= p[i] <= oz:
            p[i] = oa + (p[i] - oa + key) % 26
        elif oA <= p[i] <= oZ:
            p[i] = oA + (p[i] - oA + key) % 26
    return bytes(p)


def decode(cipher: bytes, key: int):
    return encode(cipher, 26-key)


if __name__ == '__main__':
    s = b'mshn{jhlzhy_jpwoly_lujvkl}'
    for i in range(26):
        print(decode(s, i))