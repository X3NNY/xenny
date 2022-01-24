# from xenny.ctf.crypto.modern.asymmetric.rsa.copper_smith.p_leak_attack import low_p_leak

def partial_p(p0, kbits, n):
    PR = PolynomialRing(Zmod(n), 'x')
    x = PR.gen()
    nbits = n.bit_length()
    f = (2**kbits)*x + p0
    f = f.monic()
    roots = f.small_roots(X=2**(nbits//2-kbits), beta=0.4)  # find root < 2^(nbits//2-kbits) with factor >= n^0.3
    if roots:
        x0 = roots[0]
        p = gcd((2**kbits)*x0 + p0, n)
        return ZZ(p)

def find_p(d0, kbits, e, n):
    X = var('X')
    for k in range(1, e+1):
        results = solve_mod([e*d0*X - k*X*(n-X+1) + k*n == X], 2^kbits)
        for x in results:
            p0 = ZZ(x[0])
            try:
                p = partial_p(p0, kbits, n)
                # p,q = low_p_leak(p0, n, pbits)
                if p:
                    return p
            except Exception:
                pass
