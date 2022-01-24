# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      boneh_and_durfee_attack
   Description :
   Author :         x3nny
   date :           2021/7/18
-------------------------------------------------
   Change Activity:
                    2021/7/18: Init
-------------------------------------------------
"""
__author__ = 'x3nny'
from sage.all_cmdline import *

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
        results = solve_mod([e*d0*X - k*X*(n-X+1) + k*n == X], 2**kbits)
        for x in results:
            p0 = ZZ(x[0])
            p = partial_p(p0, kbits, n)
            if p:
                return p


if __name__ == '__main__':
    # n(必须为整形才可计算) = 0x51fb3416aa0d71a430157d7c9853602a758e15462e7c08827b04cd3220c四27bbb8199ed4f5393dae43f013b68732a685defc17497f0912c886fa780dfacdfbb1461197d95a92a7a74ade874127a61411e14a901382ed3fb9d62c040c0dbaa374b5a4df06481a26da3fca271429ff10a4fc973b1c82553e3c1dd4f2f37dc24b3b
    # d0=给出的部分d(必须为整形才可计算) = 0x17c4b18f1290b6a0886eaa7bf426485a3994c5b71186fe84d5138e18de7e060db57f9580381a917fdfd171bfd159825a7d1e2800e2774f5e4449d17e6723749b

    n = 67675436138495930038587955291794936545875393540861004623773584574883114213804442800330130716284414491934727036759112376625314112545439729669100531873882029975822069580968399809536705780217420907598812455839914433470043141045447919551851701892872488410107262471823600211163797026982837582594201718874855681143
    e = 3
    c = 279116358436840586944680277601274924529608198316205227955529629010849713273120016027844880211127487505772090413968557874765704556999317230160902323292620570150480693203535190440306267731171456145948158022713266670119656726857968611653730576038607507369719554261606321424718522935536929125
    d0 = 6073962380088005462735237201070274665248258112978219756583568363468222722284990059580651266399826661735902809127738699748745981462473328880092421504223051
    p = find_p(d0, 512, e, n)
    print("found p: %d" % p)
    q = n//p
    # # print(d)
    # print("完整的d是:"+str())
    from Crypto.Util.number import *
    print(long_to_bytes(pow(c, inverse_mod(e, (q-1)*(p-1)), n)))