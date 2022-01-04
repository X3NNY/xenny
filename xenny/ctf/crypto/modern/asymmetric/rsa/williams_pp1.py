from itertools import count
from gmpy2 import gcd, isqrt

from util.timeout import timeout as t_o


def mlucas(v, a, n):
    """ Helper function for williams_pp1().  Multiplies along a Lucas sequence modulo n. """
    v1, v2 = v, (v ** 2 - 2) % n
    for bit in bin(a)[3:]: v1, v2 = ((v1 ** 2 - 2) % n, (v1 * v2 - v) % n) if bit == "0" else (
        (v1 * v2 - v) % n, (v2 ** 2 - 2) % n)
    return v1


# Recursive sieve of Eratosthenes
def primegen():
    yield 2
    yield 3
    yield 5
    yield 7
    yield 11
    yield 13
    ps = primegen()  # yay recursion
    p = ps.__next__() and ps.__next__()
    q, sieve, n = p ** 2, {}, 13
    while True:
        if n not in sieve:
            if n < q:
                yield n
            else:
                next, step = q + 2 * p, 2 * p
                while next in sieve:
                    next += step
                sieve[next] = step
                p = ps.__next__()
                q = p ** 2
        else:
            step = sieve.pop(n)
            next = n + step
            while next in sieve:
                next += step
            sieve[next] = step
        n += 2


def ilog(x, b):  # greatest integer l such that b**l <= x.
    l = 0
    while x >= b:
        x /= b
        l += 1
    return l


def attack(n, timeout=60):
    with t_o(timeout):
        try:
            for v in count(1):
                for p in primegen():
                    e = ilog(isqrt(n), p)
                    if e == 0:
                        break
                    for _ in range(e):
                        v = mlucas(v, p, n)
                    g = gcd(v - 2, n)
                    if 1 < g < n:
                        return int(g), int(n // g)  # g|n
                    if g == n:
                        break
        except TimeoutError:
            pass



if __name__ == '__main__':
    n = 22936878395364911533538150253762156299125342227773505269785563233854533376189046672957480023997170528825673941588867713541918615589640149636586419530344838982307751376764558199353644774379431998167759486243400301741765588059817544425905346814451833954744870491705733803468041358818782809689511643459640896001276832894523240197319192211042946311433803119661625519575004373285305612958236846822958081349971940386473596225699548867035153600961518507994042185901567521201496513344860022136071409998500504780788420590852310172094034690278459404629312740957973736405870002125576838233654060558183690722544711184355692861217
    print(attack(n))
    # print(attack(
    #     160403618619369740784853405475277566099157295085521281732123627794416613123342643984166030947120359756139483988734111569042122054294444739960240303565079213749999543601233610909723345193552396410793537238062325151315096286527877906836125796807589011355879825171927922525913787580432389992050039786523880417390191270847
    # ))
