# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      factor_the_modulus
   Description :
   Author :         x3nny
   date :           2022/1/5
-------------------------------------------------
   Change Activity:
                    2022/1/5: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

from Crypto.Util.number import getRandomRange
from gmpy2 import gcd, powmod, isqrt

from xenny.util.math import bsgs


def known_a_b(n, a, b):
    """
    N = 2g(2gab+a+b)+1
    """
    g = -(a + b) + isqrt(a*a + (4*n - 2)*a*b + b*b) // 4*a*b
    return 2*g*a + 1, 2*g*b + 1


def known_g(n, g):
    """
    N = 2g(2gab+a+b)+1
    """

    # g > a+b
    c = n % g
    a1 = (g*c + isqrt(2*g*g*c*c - (n - 1) + 2*g*c)) // 2*g
    a2 = (g*c - isqrt(2*g*g*c*c - (n - 1) + 2*g*c)) // 2*g

    b1 = c - a1
    b2 = c - a2

    if n % (2*g*a1+1) == 0:
        return 2*g*a1+1, 2*g*b1+1
    if n % (2*g*a2+1) == 0:
        return 2*g*a2+1, 2*g*b2+1

    # g == a+b
    a1 = (g + isqrt(g*g - (n - 1 - 2*g*g) // g*g)) // 2
    a2 = (g + isqrt(g*g - (n - 1 - 2*g*g) // g*g)) // 2

    b1 = g - a1
    b2 = g - a2

    if n % (2*g*a1+1) == 0:
        return 2*g*a1+1, 2*g*b1+1
    if n % (2*g*a2+1) == 0:
        return 2*g*a2+1, 2*g*b2+1

    y = 2 ** (2*g)
    ng = (n-1) // 2*g

    v = ng % (2*g)
    u = ng // 2*g
    c = powmod(y, u, n)
    c = bsgs(n, c, y)
    from sympy.abc import a, b
    from sympy import solve
    s = solve([u-c-a*b, v+2*g*c - a-b], [a,b], dict=True)
    a = s[0][a]
    b = s[0][b]
    return 2*g*a+1, 2*g*b+1


def big_gamma_factor(n):
    """
    N = 2g(2gab+a+b)+1
    g = N^{\gamma} and gamma \approx 1/2
    """
    f = lambda x, m: (powmod(x, m - 1, m) + 3) % m

    def pollard_rho(n):
        i = 1
        while True:
            a = getRandomRange(2, n)
            b = f(a, n)
            j = 1
            while True:
                p = gcd(abs(a - b), n)
                if p == n:
                    break
                elif p > 1:
                    return p, n // p
                else:
                    a = f(a, n)
                    b = f(f(b, n), n)
                j += 1
            i += 1

    return pollard_rho(n)


def small_gamma_factor(n):
    """
    N = 2g(2gab+a+b)+1
    g = N^{\gamma} and gamma small
    """
    from sage.all_cmdline import ecm
    res = ecm.find_factor((n-1) // 2)
    if len(res) == 2:
        return known_g(n, min(res[0], res[1]))
    return None
