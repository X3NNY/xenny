# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      extending_wiener
   Description :
   Author :         x3nny
   date :           2022/1/6
-------------------------------------------------
   Change Activity:
                    2022/1/6: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

import os
from sage.all_cmdline import *

path = os.path.join(os.path.dirname(__file__), 'rsa_extending_wiener_attack.sage')
load(path)

def attack(NN, elist, alpha=None):
    """
    alpha = bits_d / bits_n
    """
    if alpha is None:
        alpha = calcAlpha(len(elist))
    return _attack(NN, elist, alpha)

def example():
    from Crypto.Util.number import long_to_bytes, getPrime, bytes_to_long
    import uuid
    def rsa(e, n):
        m = uuid.uuid4().hex.encode()
        c = pow(bytes_to_long(m), e, n)
        return m.decode(), c
    p = getPrime(1024)
    q = getPrime(1024)

    # The modulus in RSA
    NN = p*q

    # The exponent in RSA
    e = 0x10001
    m, c = rsa(e, NN)
    print("The plaintext is:", m)

    # Theoretical upper bound in paper, but it is much smaller when actual test
    alpha = calcAlpha(3)
    print("Alpha: ",alpha)
    elist = [int(inverse_mod(getPrime(int(alpha * NN.bit_length())), (p-1) * (q-1))) for i in range(3)]
    phi = attack(NN, elist)

    if phi != 0:
        print("Found Phi: ", phi)
        d = inverse_mod(e, phi)
        print("Bingo!The message is: ", long_to_bytes(pow(c, d, NN)))

if __name__ == "__main__":
    example()