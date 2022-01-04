# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      _01248
   Description :
   Author :         x3nny
   date :           2021/6/30
-------------------------------------------------
   Change Activity:
                    2021/6/30: Init
-------------------------------------------------
"""
__author__ = 'x3nny'


def encode(content: bytes):
    p = list(content.lower())
    oa = ord('a')
    ret = ''
    for i in range(len(p)):
        num = p[i] - oa + 1
        ret += '8'*(num // 8); num = num%8
        ret += '4'*(num // 4); num = num%4
        ret += '2'*(num // 2); num = num%2
        ret += '1'*num
        ret += '0'
    return ret[:-1].encode()


def decode(cipher: bytes):
    p = cipher.split(b'0')
    ret = ''
    oa = ord('a')
    o0 = ord('0')
    for i in p:
        num = 0
        for j in i:
            num += j - o0
        if num >= 1:
            ret += chr(oa + num - 1)
    return ret.encode()