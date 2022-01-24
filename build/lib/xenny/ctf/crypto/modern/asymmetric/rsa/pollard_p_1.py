from gmpy2 import powmod, gcd
from xenny.util.timeout import timeout as t_o

def pollard(N, t):
    with t_o(t):
        try:
            a = 2
            n = 2
            while True:
                a = powmod(a, n, N)
                p = gcd(a-1, N)
                if p != 1 and p != N:
                    return p
                n += 1
        except TimeoutError:
            pass


def attack(n, timeout=60):
    return pollard(n, timeout)