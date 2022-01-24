# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      pohlig_hellman
   Description :
   Author :         x3nny
   date :           2021/10/7
-------------------------------------------------
   Change Activity:
                    2021/10/7: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

from Crypto.Util.number import long_to_bytes

def pohlig_hellman(E, P, Q):
    # pp = factor(E.order()) # P.order()
    factors, exponents = zip(*factor(E.order()))
    primes = [factors[i] ^ exponents[i] for i in range(len(factors))][:-1]

    dlogs = []
    for fac in primes:
        t = int(P.order()) // int(fac)
        dlog = discrete_log(t*Q,t*P,operation="+")
        dlogs.append(dlog)
    m = crt(dlogs, primes)
    return m

def pohlig_hellman2(P, Q):
    factors, exponents = zip(*factor(P.order()))
    primes = [factors[i] ^ exponents[i] for i in range(len(factors))][:-1]

    dlogs = []
    for fac in primes:
        t = int(P.order()) // int(fac)
        dlog = discrete_log(t*Q,t*P,operation="+")
        dlogs.append(dlog)
    m = crt(dlogs, primes)
    return m

def attack(a, b, n, p, q, spec=None):
    E = EllipticCurve(GF(n), [a, b])
    P = E.point(p)
    Q = E.point(q)
    if spec != 'P':
        return pohlig_hellman(E, P, Q)
    else:
        return pohlig_hellman2(P, Q)

if __name__ == "__main__":
    p = 146808027458411567
    A = 46056180
    B = 2316783294673
    P = [119851377153561800, 50725039619018388]
    Q = [22306318711744209, 111808951703508717]

    m = attack(A, B, p, P, Q)
    print(long_to_bytes(m))