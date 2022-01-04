# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      affine
   Description :
   Author :         x3nny
   date :           2021/10/29
-------------------------------------------------
   Change Activity:
                    2021/10/29: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

import gmpy2


def encode(s: str, a: int, b: int):
    """
    仿射加密
    :param s:
    :param a:
    :param b:
    :return:
    """
    ret = ''
    for i in s.upper():
        ret += chr(((ord(i) - 65)*a + b)%26 + 65)
    return ret


def decode(s: str, a: int, b: int):
    """
    仿射解密
    :param s:
    :param a:
    :param b:
    :return:
    """
    ret = ''
    a_inv = gmpy2.invert(a, 26)
    for i in s:
        ret += chr((ord(i) - 65 - b)*a_inv%26 + 65)
    return ret


if __name__ == '__main__':
    # s = 'flagispassword'
    # print(encode(s, 5, 7))
    print(decode('welcylk',11 ,6))
