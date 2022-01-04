from gmpy2 import *
from util.timeout import timeout as t_o


def dpdqleak(dp, dq, p, q, c):
    invp = invert(p, q)
    m1 = powmod(c, dp, p)
    m2 = powmod(c, dq, q)
    m = (((m2 - m1) * invp) % q) * p + m1
    return m


def dpleak(e, dp, n, c, timeout=60):
    with t_o(timeout):
        try:
            for x in range(1, e):
                if (e * dp - 1) % x == 0:
                    p = (e * dp - 1) // x + 1
                    if n % p == 0:
                        q = n // p
                        d = invert(e, (p - 1) * (q - 1))
                        m = powmod(c, d, n)
                        return m
        except TimeoutError:
            pass


def bige_dpleak(e, dp, n, c, m=1000000007):
    p = gcd(powmod(m, dp, n) - m, n)
    q = n // p
    d = invert(e, (p - 1) * (q - 1))
    m = powmod(c, d, n)
    return m


def attack(dp, c, dq=None, p=None, q=None, e=None, n=None, m=1000000007):
    if dq is not None and \
            p is not None and \
            q is not None:
        return dpdqleak(dp, dq, p, q, c)
    elif e is not None and \
            n is not None:
        if e < 10 ** 10:
            return dpleak(e, dp, n, c)
        else:
            return bige_dpleak(e, dp, n, c, m)



from Crypto.Util.number import *
e = 65537
n = 248254007851526241177721526698901802985832766176221609612258877371620580060433101538328030305219918697643619814200930679612109885533801335348445023751670478437073055544724280684733298051599167660303645183146161497485358633681492129668802402065797789905550489547645118787266601929429724133167768465309665906113
dp = 905074498052346904643025132879518330691925174573054004621877253318682675055421970943552016695528560364834446303196939207056642927148093290374440210503657

c = 140423670976252696807533673586209400575664282100684119784203527124521188996403826597436883766041879067494280957410201958935737360380801845453829293997433414188838725751796261702622028587211560353362847191060306578510511380965162133472698713063592621028959167072781482562673683090590521214218071160287665180751

m = attack(dp, c, e=e, n=n)

print(long_to_bytes(m))