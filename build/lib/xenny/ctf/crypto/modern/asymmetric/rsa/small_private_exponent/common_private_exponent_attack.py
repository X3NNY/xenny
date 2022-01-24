# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      common_private_exponent_attack
   Description :
   Author :         x3nny
   date :           2022/1/6
-------------------------------------------------
   Change Activity:
                    2022/1/6: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

from sage.all_cmdline import *

def attack(e, N):
    r = len(e)
    # assert len(e) == len(N) == r
    M = int(sqrt(N[r-1]))
    B = matrix([M, *e]).stack(matrix(ZZ, r, 1).augment(matrix(ZZ, r, r, lambda i, j: -N[i]*(i==j))))
    B = B.LLL()
    d = abs(B[0][0]) // M
    return d

def example():
    e1, N1 = 587438623, 2915050561
    e2, N2 = 2382816879, 3863354647
    e3, N3 = 2401927159, 3943138939
    e = [e1, e2, e3]
    N = [N1, N2, N3]
    d = attack(e, N)
    print(d)

if __name__ == '__main__':
    example()