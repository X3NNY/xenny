from gmpy2 import *


class LCG:
    def __init__(self, a, b, n, seed):
        self.a = a
        self.b = b
        self.n = n
        self.state = seed

    def extract_number(self):
        self.state = (self.a*self.state + self.b) % self.n
        return self.state


def recover_seed(a, b, n, output, index):
    """
    恢复种子
    :param a:
    :param b:
    :param n:
    :param output:
    :return:
    """
    ani = invert(a, n)
    seed = output[-1]
    for i in range(index):
        seed = (ani*(seed - b)%n + n) % n
    return seed


def recover_b(a, n, output):
    """
    恢复b
    :param a:
    :param n:
    :param output: len(output) >= 2
    :return:
    """
    b = (output[1] - a*output[0]%n + n) % n
    return b


def recover_a(n, output):
    """
    恢复a
    :param n:
    :param output: len(output) >= 3
    :return:
    """
    a = (output[2] - output[1]) * invert((output[1] - output[0]), n) % n
    return a


def recover_n(output):
    """
    恢复n
    :param output: len(output) >= 6
    :return:
    """
    t = []
    l = len(output)
    for i in range(1, l):
        t.append(output[i] - output[i-1])
    n = 0
    for i in range(l - 2):
        n = gcd((t[i+1]*t[i-1] - t[i]*t[i]), (t[i+2]*t[i] - t[i+1]*t[i+1]))
        if n != 1:
            return n



def attack(n = None, a = None, b = None, seed = None, output=None, index = None):
    if output is None:
        raise Exception("output can't be None")
    if n is None:
        n = recover_n(output)
    if a is None:
        a = recover_a(n, output)
    if b is None:
        b = recover_b(a, n, output)

    if index is None:
        return recover_seed(a, b, n, output, len(output))

    return recover_seed(a, b, n, output, index)