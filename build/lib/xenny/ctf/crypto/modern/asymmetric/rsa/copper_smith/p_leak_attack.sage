# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      p_leak_attack
   Description :
   Author :         x3nny
   date :           2021/7/18
-------------------------------------------------
   Change Activity:
                    2021/7/18: Init
-------------------------------------------------
"""

from Crypto.Util.number import *

def high_p_leak(pbar, n, bits):
    PR.<x> = PolynomialRing(Zmod(n))
    f = x + pbar
    roots = f.small_roots(X=2^bits, beta=0.4) # find root < 2^kbits with factor >= n^0.4
    if not roots:
        return None, None
    p = int(roots[0]+pbar)
    return p, n // p

def low_p_leak(pbar, n, bits):
    PR.<x> = PolynomialRing(Zmod(n))
    ZmodN = Zmod(n)
    f = x*ZmodN(power(2, pbar.bit_length())) + pbar
    f = f.monic()
    roots = f.small_roots(X=2^bits, beta=0.4) # find root < 2^kbits with factor >= n^0.4
    if not roots:
        return None, None
    p = int(roots[0]*ZmodN(power(2, pbar.bit_length())) + pbar)
    return p, n // p

def attack(pbar, n, bits=None):
    if bits is None:
        bits = (n.bit_length() // 2) - pbar.bit_length()
    p,q = high_p_leak(pbar, n, bits)
    if p is None:
        return low_p_leak(pbar, n, bits)
    return p, q