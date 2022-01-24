from Crypto.Util.number import long_to_bytes
from gmpy2 import invert, powmod, gcdext

def attack(n, e1, e2, c1, c2):
    g, s1, s2 = gcdext(e1, e2)
    if s1 < 0:
        s1 = -s1
        c1 = invert(c1, n)
    elif s2 < 0:
        s2 = -s2
        c2 = invert(c2, n)

    m = powmod(c1, s1, n) * powmod(c2, s2, n) % n
    return m
