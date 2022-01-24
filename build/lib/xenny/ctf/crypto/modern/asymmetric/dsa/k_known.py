import gmpy2


def attack(r, k, s, hm, q):
    x = gmpy2.invert(r, q) * (k * s - hm) % q
    return x