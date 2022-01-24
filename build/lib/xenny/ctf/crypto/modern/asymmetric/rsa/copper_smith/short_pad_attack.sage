# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      short_pad_attack
   Description :
   Author :         x3nny
   date :           2021/7/23
-------------------------------------------------
   Change Activity:
                    2021/7/23: Init
-------------------------------------------------
"""
__author__ = 'x3nny'


# Franklin-Reiter attack against RSA.
# If two messages differ only by a known fixed difference between the two messages
# and are RSA encrypted under the same RSA modulus N
# then it is possible to recover both of them.

# Inputs are modulus, known difference, ciphertext 1, ciphertext2.
# Ciphertext 1 corresponds to smaller of the two plaintexts. (The one without the fixed difference added to it)


def franklinReiter(n,e,r,c1,c2):
    R.<X> = Zmod(n)[]
    f1 = X^e - c1
    f2 = (X + r)^e - c2
    # coefficient 0 = -m, which is what we wanted!
    return Integer(n-(compositeModulusGCD(f1,f2)).coefficients()[0])

# GCD is not implemented for rings over composite modulus in Sage
# so we do our own implementation. Its the exact same as standard GCD, but with
# the polynomials monic representation
def compositeModulusGCD(a, b):
    if(b == 0):
        return a.monic()
    else:
        return compositeModulusGCD(b, a % b)

def CoppersmithShortPadAttack(e,n,C1,C2,eps=1/30):
    """
    Coppersmith's Shortpad attack!
    Figured out from: https://en.wikipedia.org/wiki/Coppersmith's_attack#Coppersmith.E2.80.99s_short-pad_attack
    """
    P.<x,y> = PolynomialRing(ZZ)
    ZmodN = Zmod(n)
    g1 = x^e - C1
    g2 = (x+y)^e - C2
    res = g1.resultant(g2)
    P.<y> = PolynomialRing(ZmodN)
    # Convert Multivariate Polynomial Ring to Univariate Polynomial Ring
    rres = 0
    for i in range(len(res.coefficients())):
        rres += res.coefficients()[i]*(y^(res.exponents()[i][1]))

    diff = rres.small_roots(epsilon=eps)
    if diff:
        return diff[0]
    return None

def another_get_diff(e, n, c1, c2):
    PRxy.<x, y> = PolynomialRing(Zmod(n))
    PRx.<xn> = PolynomialRing(Zmod(n))
    PRZZ.<xz,yz> = PolynomialRing(Zmod(n))

    g1 = x ** e - c1
    g2 = (x + y) ** e - c2
    q1 = g1.change_ring(PRZZ)
    q2 = g2.change_ring(PRZZ)
    h = q2.resultant(q1)
    h = h.univariate_polynomial()
    h = h.change_ring(PRx).subs(y=xn)
    h = h.monic()
    kbits = n.bit_length() // (2 * e * e)
    diff = h.small_roots(X=2^kbits, beta=0.5)[0]  # find root < 2^kbits with factor >= n^0.5
    return diff

def getdiff(e, n, c1, c2, eps):
    diff = CoppersmithShortPadAttack(e, n, c1, c2, eps)
    if diff:
        return diff
    return another_get_diff(e, n, c1, c2)

def attack(e, n, c1, c2, r=None, eps=1/25):
    if r is None:
        r = getdiff(e, n, c1, c2, eps)
    m = franklinReiter(n,e,r,c1,c2)
    return m