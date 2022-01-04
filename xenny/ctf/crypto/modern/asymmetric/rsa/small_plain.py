import gmpy2


def attack(e: int, c: int):
    return gmpy2.iroot(c, e)[0]