from gmpy2 import *
from xenny.util.timeout import timeout as t_o


def dpdqleak(dp, dq, p, q, c):
    invp = invert(p, q)
    m1 = powmod(c, dp, p)
    m2 = powmod(c, dq, q)
    m = (((m2 - m1) * invp) % q) * p + m1
    return m


def dpleak(e, dp, n, c, timeout=60):
    with t_o(timeout):
        try:
            for x in range(1, e):
                if (e * dp - 1) % x == 0:
                    p = (e * dp - 1) // x + 1
                    if n % p == 0:
                        q = n // p
                        d = invert(e, (p - 1) * (q - 1))
                        m = powmod(c, d, n)
                        return m
        except TimeoutError:
            pass


def bige_dpleak(e, dp, n, c, m=1000000007):
    p = gcd(powmod(m, e*dp, n) - m, n)
    if p != 1:
        q = n // p
        d = invert(e, (p - 1) * (q - 1))
        m = powmod(c, d, n)
        return m
    return None


def attack(dp, c, dq=None, p=None, q=None, e=None, n=None, m=1000000007):
    if dq is not None and \
            p is not None and \
            q is not None:
        return dpdqleak(dp, dq, p, q, c)
    elif e is not None and \
            n is not None:
        if e < 10 ** 10:
            return dpleak(e, dp, n, c)
        else:
            return bige_dpleak(e, dp, n, c, m)
