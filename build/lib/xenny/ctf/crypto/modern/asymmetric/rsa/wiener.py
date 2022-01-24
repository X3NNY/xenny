from Crypto.Util.number import long_to_bytes
from gmpy2 import *


class ContinuedFraction():
    def __init__(self, numerator, denumerator):
        self.numberlist = []  # number in continued fraction
        self.fractionlist = []  # the near fraction list
        self.GenerateNumberList(numerator, denumerator)
        self.GenerateFractionList()

    def GenerateNumberList(self, numerator, denumerator):

        while numerator != 1:
            quotient = numerator // denumerator
            remainder = numerator % denumerator
            self.numberlist.append(quotient)
            numerator = denumerator
            denumerator = remainder

    def GenerateFractionList(self):
        self.fractionlist.append([self.numberlist[0], 1])
        for i in range(1, len(self.numberlist)):
            numerator = self.numberlist[i]
            denumerator = 1
            for j in range(i):
                temp = numerator
                numerator = denumerator + numerator * self.numberlist[i - j - 1]
                denumerator = temp
            self.fractionlist.append([numerator, denumerator])


def Solve(a, b, c):
    """solve ax^2+bx+c=0 , return x1 , x2"""
    delta = b ** 2 - 4 * a * c
    if delta < 0:
        return 0
    if is_square(delta):
        sqr_delta = isqrt(delta)
        temp1 = -b + sqr_delta
        temp2 = -b - sqr_delta
        if temp1 % (2 * a) != 0 or temp2 % (2 * a) != 0:
            return 0
        else:
            return [temp1 // (2 * a), temp2 // (2 * a)]
    else:
        return 0


def attack(n, e):
    a = ContinuedFraction(e, n)
    for i in a.fractionlist:
        k = i[0]
        d = i[1]
        if k == 0:
            continue
        phi = (d * e - 1) // k
        b = phi - n - 1
        temp = Solve(1, b, n)
        if isinstance(temp, list):
            p, q = temp
            return d, p, q
    return None, None, None
