def exgcd(a, b):
    """
    Solve a*x + b*y = gcd(a, b)
    :param a:
    :param b:
    :return: gcd, x, y
    """
    if a == 0:
        return b, 0, 1
    g, y, x = exgcd(b % a, a)
    return g, x-(b//a)*y, y
