# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      hill
   Description :
   Author :         x3nny
   date :           2021/10/29
-------------------------------------------------
   Change Activity:
                    2021/10/29: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

import numpy as np
import gmpy2

def encode(s: str, key: str):
    """
    希尔加密
    :param s: 长度为n的字符串
    :param key: 长度为n*n的字符串
    :return:
    """
    ss = []
    for i in s:
        ss.append(ord(i.upper()) - 65)

    keys = []
    for i in range(len(s)):
        keys.append([])
        for j in range(len(s)):
            keys[i].append(ord(key[i*len(s) + j].upper())-65)

    keys = np.array(keys)
    ss = np.array(ss)

    ret = ''
    for i in np.dot(keys, ss):
        ret += chr(65 + i % 26)
    return ret


def decode(s: str, key: str):
    """
    希尔加密
    :param s: 长度为n的字符串
    :param key: 长度为n*n的字符串
    :return:
    """
    ss = []
    for i in s:
        ss.append(ord(i.upper()) - 65)

    keys = []
    for i in range(len(s)):
        keys.append([])
        for j in range(len(s)):
            keys[i].append(ord(key[i*len(s) + j].upper())-65)

    keys = np.array(keys)
    det = int(np.linalg.det(keys))
    keys_inv = np.linalg.inv(keys)

    keys_star = keys_inv * det
    det_inv = int(gmpy2.invert(det, 26))
    keys = (det_inv * keys_star) % 26

    ss = np.array(ss)

    ret = ''
    for i in np.dot(keys, ss):
        ret += chr(65 + int(i + 1e-6) % 26)
    return ret

if __name__ == '__main__':
    # s = 'ABC'
    key = 'GYBNQKURP'
    # print(encode(s, key))
    print(decode('AKV',key))
