# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      playfair
   Description :
   Author :         x3nny
   date :           2021/10/29
-------------------------------------------------
   Change Activity:
                    2021/10/29: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

from pycipher import Playfair
from string import ascii_uppercase


def encode(s: str, key: str):
    key = key.upper()
    skey = ''
    for i in key:
        if i not in skey:
            skey += i
    for i in ascii_uppercase:
        if i == 'J': continue
        if i not in key:
            skey += i

    return Playfair(skey).encipher(s)


def decode(s: str, key: str):
    key = key.upper()
    skey = ''
    for i in key:
        if i not in skey:
            skey += i
    for i in ascii_uppercase:
        if i == 'J': continue
        if i not in key:
            skey += i

    return Playfair(skey).decipher(s)

if __name__ == '__main__':
    s = 'flagispass'
    print(encode(s, 'hello'))
    print(decode(encode(s, 'hello'),'hello'))