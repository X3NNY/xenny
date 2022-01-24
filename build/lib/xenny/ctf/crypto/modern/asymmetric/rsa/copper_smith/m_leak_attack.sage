# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      m_leak_attack
   Description :
   Author :         x3nny
   date :           2021/7/18
-------------------------------------------------
   Change Activity:
                    2021/7/18: Init
-------------------------------------------------
"""

from Crypto.Util.number import *

def high_m_leak(mbar, c, n, e, bits):
    PR.<x> = PolynomialRing(Zmod(n))
    f = (mbar + x)^e - c
    roots = f.small_roots(X=2^bits, beta=1) # find root < 2^kbits with factor >= n^0.4
    if not roots:
        return None, None
    m = int(roots[0]+mbar)
    return m

def low_m_leak(mbar, c, n, e, bits):
    PR.<x> = PolynomialRing(Zmod(n))
    ZmodN = Zmod(n)
    f = (x*ZmodN(power(2, mbar.bit_length())) + mbar)^e - c
    f = f.monic()
    roots = f.small_roots(X=2^bits, beta=1) # find root < 2^kbits with factor >= n^0.4
    if not roots:
        return None, None
    m = roots[0]+mbar
    return m

def attack(mbar, c, n, e, bits=None):
    if bits is None:
        raise Exception('bits can\'t be None.')
    m = high_m_leak(mbar, c, n, e, bits)
    if m is None:
        return low_m_leak(mbar, c, n, e, bits)
    return m