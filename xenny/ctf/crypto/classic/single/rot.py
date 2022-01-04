try:
    from . import caesar
except:
    import caesar


def rot5(content: bytes):
    p = list(content)
    for i in range(len(p)):
        if ord('0') <= p[i] <= ord('9'):
            p[i] = ord('0') + (p[i] - ord('0') + 5) % 10
    return bytes(p)


def rot13(content: bytes):
    return caesar.encode(content, 13)


def rot18(content: bytes):
    return rot5(rot13(content))


def rot47(content: bytes):
    p = list(content)
    for i in range(len(p)):
        if 33 <= p[i] <= 126:
            p[i] = 33 + (p[i] - 33 + 47) % (126 - 33 + 1)
    return bytes(p)

if __name__ == '__main__':
    s = rot47(b'v)*L*_F0<}@H0>F49023@FE0#@EN')
    print(s)
    # print(rot18(s))