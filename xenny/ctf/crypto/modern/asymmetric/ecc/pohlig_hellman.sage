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

def pohlig_hellman(a, b, n, p, q):
    E = EllipticCurve(GF(n), [a, b])
    P = E.point(p)
    Q = E.point(q)
    pp = factor(E.order()) # P.order()
    dlogs = []
    f = []
    for i in pp:
        tmp = int(i[0])**int(i[1])
        t = int(P.order()) // tmp
        dlog = discrete_log(t * Q, t * P, operation='+')
        f.append(tmp)
        dlogs.append(dlog)
    m = crt(dlogs, f)
    return m

def attack(a, b, n, p, q):
    return pohlig_hellman(a,b,n,p,q)

if __name__ == "__main__":
    p = 146808027458411567
    A = 46056180
    B = 2316783294673
    P = [119851377153561800, 50725039619018388]
    Q = [22306318711744209, 111808951703508717]

    m = attack(A, B, p, P, Q)
    print(long_to_bytes(m))