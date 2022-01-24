# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      williams_and_schmid_some_remarks_concerning
   Description :
   Author :         x3nny
   date :           2022/1/6
-------------------------------------------------
   Change Activity:
                    2022/1/6: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

from Crypto.Util.number import getPrime
from gmpy2 import is_prime, invert, powmod, gcd


def prime_gen():
    Q = getPrime(168)
    P = getPrime(168)
    x = invert(P, Q)
    for miu in range(100000):
        q = miu * (2 * Q * P) + 2 * P * x + 1
        p = miu * (4 * Q * P) + 4 * P * x + 3
        if is_prime(q) and is_prime(p):
            return q, p

def key_gen():
    g = e = 0x10001
    # p = 221653739318859595167225381203666210391549468559991916323154342583649061535907#prime_gen()
    # q = 191519573353607170273871810379049103111742792135913035013934992306073451523799#prime_gen()
    #
    # n = p-1
    # F = lambda x: x-1
    # P = lambda x: F(powmod(x, n, p))
    # print(P(e) % p)
    q1, p1 = prime_gen()
    q2, p2 = prime_gen()

    d = invert(e, 2 * q1 * q2)

    r = p1*p2
    print('r:', r)
    c = powmod(123, e, r)

    for i in range(1, 1000000):
        g = gcd(powmod(powmod(c, e, r), i, r)-c, r)
        if g != 1:
            print(g)
            print('m:',powmod(powmod(c, e, r), i-1, r))

if __name__ == '__main__':
    key_gen()

