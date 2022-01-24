from gmpy2 import invert, iroot


def attack(e, n_list, c_list):
    n = 1
    for i in n_list:
        n *= i
    N = []
    for i in n_list:
        N.append(n//i)

    t = []
    for i in range(len(n_list)):
        t.append(invert(N[i], n_list[i]))

    summary = 0
    for i in range(len(n_list)):
        summary = (summary + c_list[i]*t[i]*N[i]) % n

    summary = iroot(summary, e)
    return summary