def encode(content: bytes):
    p = list(content)
    oa = ord('a')
    oz = ord('z')
    oA = ord('A')
    oZ = ord('Z')
    for i in range(len(p)):
        if oa <= p[i] <= oz:
            p[i] = oa + 25 - p[i] + oa
        elif oA <= p[i] <= oZ:
            p[i] = oA + 25 - p[i] + oA
    return bytes(p)


def decode(cipher: bytes):
    return encode(cipher)


if __name__ == '__main__':
    s = b'gsv_pvb_rh_zgyzhs'
    print(decode(s))