import gmpy2


def attack(e: int, c: int, n: int=None, max_k: int=1000000):
    if n is None:
        return gmpy2.iroot(c, e)
    for i in range(max_k):
        potential_value, exact_root = gmpy2.iroot(c + (n * i), e)
        if exact_root:
            return potential_value, exact_root
    return False, 0