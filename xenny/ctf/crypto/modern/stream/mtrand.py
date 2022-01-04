from random import Random
from gmpy2 import invert


def _int32(x):
    return int(0xFFFFFFFF & x)


class MT19937:
    # 根据seed初始化624的state
    def __init__(self, seed):
        self.mt = [0] * 624
        self.mt[0] = seed
        self.mti = 0
        for i in range(1, 624):
            self.mt[i] = _int32(1812433253 * (self.mt[i - 1] ^ self.mt[i - 1] >> 30) + i)


    # 提取伪随机数
    def extract_number(self):
        if self.mti == 0:
            self.twist()
        y = self.mt[self.mti]
        y = y ^ y >> 11
        y = y ^ y << 7 & 2636928640
        y = y ^ y << 15 & 4022730752
        y = y ^ y >> 18
        self.mti = (self.mti + 1) % 624
        return _int32(y)

    # 对状态进行旋转
    def twist(self):
        for i in range(0, 624):
            y = _int32((self.mt[i] & 0x80000000) + (self.mt[(i + 1) % 624] & 0x7fffffff))
            self.mt[i] = (y >> 1) ^ self.mt[(i + 397) % 624]
            if y % 2 != 0:
                self.mt[i] = self.mt[i] ^ 0x9908b0df


def inverse_right(res, shift, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift
    return tmp


def inverse_left(res, shift, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp << shift


def inverse_right_mask(res, shift, mask, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp >> shift & mask
    return tmp


def inverse_left_mask(res, shift, mask, bits=32):
    tmp = res
    for i in range(bits // shift):
        tmp = res ^ tmp << shift & mask
    return tmp


# 通过mt中的任一位逆向seed
def inv_init(last, index=623):
    n = 1 << 32
    inv = invert(1812433253, n)
    for i in range(index, 0, -1):
        last = ((last - i) * inv) % n
        last = _int32(inverse_right(last, 30))
    return last


# 逆向提取伪随机数
def inv_extract_number(y):
    y = inverse_right(y, 18)
    y = inverse_left_mask(y, 15, 4022730752)
    y = inverse_left_mask(y, 7, 2636928640)
    y = inverse_right(y, 11)
    return y & 0xffffffff


# 逆向提取state，多轮twist情况
def inv_twist(cur):
    """
    恢复state
    :param cur: length >= 1000
    :return:
    """
    high = 0x80000000
    low = 0x7fffffff
    mask = 0x9908b0df
    state = cur
    for i in range(3, -1, -1):
        tmp = state[i + 624] ^ state[i + 397]
        # recover Y,tmp = Y
        if tmp & high == high:
            tmp ^= mask
            tmp <<= 1
            tmp |= 1
        else:
            tmp <<= 1
        # recover highest bit
        res = tmp & high
        # recover other 31 bits,when i =0,it just use the method again it so beautiful!!!!
        tmp = state[i - 1 + 624] ^ state[i + 396]
        # recover Y,tmp = Y
        if tmp & high == high:
            tmp ^= mask
            tmp <<= 1
            tmp |= 1
        else:
            tmp <<= 1
        res |= (tmp) & low
        state[i] = res
    return state


# other impl
# def backtrace(cur):
#     high = 0x80000000
#     low = 0x7fffffff
#     mask = 0x9908b0df
#     state = cur
#     for i in range(623,-1,-1):
#         tmp = state[i]^state[(i+397)%624]
#         # recover Y,tmp = Y
#         if tmp & high == high:
#             tmp ^= mask
#             tmp <<= 1
#             tmp |= 1
#         else:
#             tmp <<=1
#         # recover highest bit
#         res = tmp&high
#         # recover other 31 bits,when i =0,it just use the method again it so beautiful!!!!
#         tmp = state[i-1]^state[(i+396)%624]
#         # recover Y,tmp = Y
#         if tmp & high == high:
#             tmp ^= mask
#             tmp <<= 1
#             tmp |= 1
#         else:
#             tmp <<=1
#         res |= (tmp)&low
#         state[i] = res
#     return state
def recover_state(record):
    """
    恢复624个state，即可预测后面的随机数
    :param record: 624个随机数
    :return:
    """
    state = [inv_extract_number(i) for i in record]
    # gen = Random()
    # gen.setstate((3, tuple(state + [0]), None))
    return state

def recover_mt(record) -> Random:
    """
    恢复624个state，即可预测后面的随机数
    :param record: 624个随机数
    :return:
    """
    state = [inv_extract_number(i) for i in record][:624]
    gen = Random()
    gen.setstate((3, tuple(state + [0]), None))
    return gen

# from sage.all import *
# def buildT():
#     rng = Random()
#     T = matrix(GF(2),32,32)
#     for i in range(32):
#         s = [0]*624
#         # 构造特殊的state
#         s[0] = 1<<(31-i)
#         rng.setstate((3,tuple(s+[0]),None))
#         tmp = rng.getrandbits(32)
#         # 获取T矩阵的每一行
#         row = vector(GF(2),[int(x) for x in bin(tmp)[2:].zfill(32)])
#         T[i] = row
#     return T
# def reverse(T,leak):
#     Z = vector(GF(2),[int(x) for x in bin(leak)[2:].zfill(32)])
#     X = Z*(T**-1) # T.solve_left(Z)
#     state = int(''.join([str(i) for i in X]),2)
#     return state
# def test():
#     rng = Random()
#     # 泄露信息
#     leak = [rng.getrandbits(32) for i in range(32)]
#     originState = [i for i in rng.getstate()[1][:32]]
#     # 构造矩阵T
#     T = buildT()
#     recoverState = [reverse(T,i) for i in leak]
#     print(recoverState,originState)
# test()


# mt = MT19937(1825637141)
# print(mt.mt)
# print(mt.extract_number())
# print(mt.extract_number())
# print(inv_init(mt.mt[623]))
# for i in range(227):
#     mt.extract_number()
# print(mt.extract_number())
# print(mt.extract_number())