# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      tap
   Description :
   Author :         x3nny
   date :           2021/10/29
-------------------------------------------------
   Change Activity:
                    2021/10/29: Init
-------------------------------------------------
"""
__author__ = 'x3nny'


def encode(s: str):
    """
    敲击码编码
    :param s: 待编码
    :return:
    """
    ret = []
    for i in s:
        tmp = i.upper()
        if tmp == 'K':
            tmp = 3
        else:
            tmp = ord(tmp) - 65 + (1 if tmp < 'K' else 0)

        ret.append(
            '%d%d' % ((tmp-1)//5+1,5 if tmp%5 == 0 else tmp%5)
        )
    return ' '.join(ret)


def decode(s: str):
    """
    敲击码解码
    :param s: 待解码
    :return:
    """
    s = s.split(' ')
    ret = ''
    for i in s:
        tmp = int(i)
        r,c = tmp//10, tmp%10
        tmp = (r-1)*5 + c
        ret += chr(65 - 1 + tmp + (1 if tmp > 10 else 0))
    return ret


if __name__ == '__main__':
    s = 'passwordishello'
    print(encode(s))
    print(decode(encode(s)))