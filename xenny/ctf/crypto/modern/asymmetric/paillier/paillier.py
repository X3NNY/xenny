from random import randint
from tkinter.messagebox import NO
from gmpy2 import gcd, powmod, invert, lcm
from Crypto.Util.number import getPrime

L = lambda x, n: (x-1)//n

def encrypt(m, n, g):
    """
        @param m: m < n
        @param n: public key N
        @param g: public key G
    """
    r = randint(1, g-1)
    while gcd(r, n) != 1:
        r = randint(1, g-1)
    mod = n*n
    c = powmod(g, m, mod) * powmod(r, n, mod) % mod
    return c


def decrypt(c, p=None, q=None, n=None, g=None, lam=None, mu=None):
    """
        @param c:
        @param p, q: n = p*q
        @param n, g: public key
        @param lam, mu: private key
    """
    if n is None and p is not None and q is not None:
        n = p*q
    if lam is None and p is not None and q is not None:
        lam = lcm(p-1, q-1)
    if mu is None and g is not None and lam is not None and n is not None:
        mu = invert(L(pow(g,lam , n**2) , n) , n**2)
    return L(powmod(c , lam , n**2) , n) * mu % n


def gen(bits=1024):
    p = getPrime(bits//2)
    q = getPrime(bits//2)
    n = p*q
    phi = (p-1)*(q-1)
    lcm = phi // gcd(p-1, q-1)
    g = randint(1, n*n-1)
    t = L(powmod(g, lcm, n*n), n)
    while gcd(t, n) != 1:
        g = randint(1, n*n-1)
        t = L(powmod(g, lcm, n*n), n)
    mu = invert(t, n)
    return (n, g), (lcm, mu)