from sage.stats.distributions.discrete_gaussian_polynomial import DiscreteGaussianDistributionPolynomialSampler as d_gauss

# flag = bytearray(input().encode())
# flag = list(flag)

n = 128
q = 40961

## Finite Field of size q.
F = GF(q)

## Univariate Polynomial Ring in y over Finite Field of size q
R.<y> = PolynomialRing(F)

## Univariate Quotient Polynomial Ring in x over Finite Field of size 40961 with modulus b^n + 1
S.<x> = R.quotient(y^n + 1)

def gen_small_poly():
    sigma = 2/sqrt(2*pi)
    d = d_gauss(S, n, sigma)
    return d()

def gen_large_poly():
    return S.random_element()
t = 128

def key_gen():
    r1, r2 = gen_small_poly(), gen_small_poly()

    p = r1 - t*r2
    return p, r2


def encrypt(p, m):
    e1, e2, e3 = gen_small_poly(), gen_small_poly(), gen_small_poly()
    c1 = t*e1 + e2
    c2 = p*e1+ e3 + m*(q//2)
    return c1, c2


def decrypt(s, c1, c2):
    m = c1*s + c2
    return m

p, s = key_gen()
c1, c2 = encrypt(p, 1)
# print(c1,c2)
print(decrypt(s, c1, c2))


def PublicKeygen(A, s):
    e = gen_small_poly()

    b = A*s + e
