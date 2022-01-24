import gmpy2


def attack(r, s1, s2, hm1, hm2, q):
    k = (hm1-hm2)*gmpy2.invert(s1-s2,q)%q
    x = gmpy2.invert(r,q)*(k*s1-hm1)%q
    return k, x
