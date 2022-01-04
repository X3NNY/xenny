# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      morse
   Description :
   Author :         x3nny
   date :           2021/10/29
-------------------------------------------------
   Change Activity:
                    2021/10/29: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

morse_table = {
    'A': '.-',      'N': '-.',      '.': '.-.-.-', '+': '.-.-.',    '1': '.----',
    'B': '-...',    'O': '---',     ',': '--..--', '_': '..--.-',   '2': '..---',
    'C': '-.-.',    'P': '.--.',    ':': '---...', '$': '...-..-',  '3': '...--',
    'D': '-..',     'Q': '--.-',    '"': '.-..-.', '&': '.-...',    '4': '....-',
    'E': '.',       'R': '.-.',     '\'': '.----.','/': '-..-.',    '5': '.....',
    'F': '..-.',    'S': '...',     '!': '-.-.--',                  '6': '-....',
    'G': '--.',     'T': '-',       '?': '..--..',                  '7': '--...',
    'H': '....',    'U': '..-',     '@': '.--.-.',                  '8': '---..',
    'I': '..',      'V': '...-',    '-': '-....-',                  '9': '----.',
    'J': '.---',    'W': '.--',     ';': '-.-.-.',                  '0': '-----',
    'K': '-.-',     'X': '-..-',    '(': '-.--.',
    'L': '.-..',    'Y': '-.--',    ')': '-.--.-',
    'M': '--',      'Z': '--..',    '=': '-...-',
}

morse_table_rev = {v: k for k, v in morse_table.items()}


def encode(s: str, dot='.', line='-', separator=' ', strict: bool = False):
    """
    摩斯编码
    :param s: 待加密内容
    :param dot: 点
    :param line: 线
    :param separator: 分隔符
    :param strict: 是否保留错误字符
    :return:
    """

    ret = []
    for i in s:
        if i.upper() in morse_table:
            ret.append(morse_table[i.upper()])
        elif strict:
            ret.append(i)

    ret = separator.join(ret)

    if dot != '.':
        ret = ret.replace('.', dot)

    if line != '-':
        ret = ret.replace('-', line)

    return ret


def decode(s: str, dot='.', line='-', separator=' ', strict: bool = False):
    """
    摩斯解码
    :param s: 待加密内容
    :param dot: 点
    :param line: 线
    :param separator: 分隔符
    :param strict: 是否保留错误字符
    :return:
    """
    if dot != '.':
        s = s.replace(dot, '.')

    if line != '-':
        s = s.replace(line, '-')
    s = s.split(separator)
    ret = ''
    for i in s:
        if i in morse_table_rev:
            ret += morse_table_rev[i]
        elif strict:
            ret += i
    return ret


if __name__ == '__main__':
    s = 'flag:this_is_flag'
    # print(encode(s))
    print(decode('.... . .-. . ..--.- .. ... ..--.- .--. .- ... ... .-- --- .-. -..'))
