from gmpy2 import powmod, invert
from Crypto.Util.number import *


def attack(c, n, p, q):
    c1 = powmod(c, (p+1)//4, p)
    c2 = powmod(c, (q+1)//4, q)
    cp1 = p - c1
    cp2 = q - c2

    t1 = invert(p, q)
    t2 = invert(q, p)

    m1 = (q*c1*c2 + p*c2*t1) % n
    m2 = (q*c1*t2 + p*cp2*t1) % n
    m3 = (q*cp1*t2 + p*c2*t1) % n
    m4 = (q*cp1*t2 + p*cp2*t1) % n

    return m1, m2, m3, m4
p = 275127860351348928173285174381581152299
q = 319576316814478949870590164193048041239
n = p*q
c = open('/Users/x3nny/Downloads/hardRSA/flag.enc', 'rb').read()
c = bytes_to_long(c)
m = attack(c,n,p,q)
# print(m)
for i in m:
    print(long_to_bytes(i))