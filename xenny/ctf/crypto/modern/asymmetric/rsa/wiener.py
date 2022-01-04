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

n = 101991809777553253470276751399264740131157682329252673501792154507006158434432009141995367241962525705950046253400188884658262496534706438791515071885860897552736656899566915731297225817250639873643376310103992170646906557242832893914902053581087502512787303322747780420210884852166586717636559058152544979471
e = 46731919563265721307105180410302518676676135509737992912625092976849075262192092549323082367518264378630543338219025744820916471913696072050291990620486581719410354385121760761374229374847695148230596005409978383369740305816082770283909611956355972181848077519920922059268376958811713365106925235218265173085

d, p, q = attack(n, e)

c= powmod(123456, e, n)
print(powmod(c, d, n))
print(d)

# print(long_to_bytes(powmod(c,d,n)))