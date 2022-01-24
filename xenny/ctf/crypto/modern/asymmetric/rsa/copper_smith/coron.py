'''
    https://github.com/ubuntor/coppersmith-algorithm/blob/main/coppersmith.sage
'''


# This file was *autogenerated* from the file xenny/ctf/crypto/modern/asymmetric/rsa/copper_smith/coron.sage
from sage.all_cmdline import *   # import sage library

_sage_const_2 = Integer(2); _sage_const_0 = Integer(0); _sage_const_1 = Integer(1)
def coron(pol, X, Y, k=_sage_const_2 , debug=False):
    """
    Returns all small roots of pol.
    Applies Coron's reformulation of Coppersmith's algorithm for finding small
    integer roots of bivariate polynomials modulo an integer.
    Args:
        pol: The polynomial to find small integer roots of.
        X: Upper limit on x.
        Y: Upper limit on y.
        k: Determines size of lattice. Increase if the algorithm fails.
        debug: Turn on for debug print stuff.
    Returns:
        A list of successfully found roots [(x0,y0), ...].
    Raises:
        ValueError: If pol is not bivariate
    """

    if pol.nvariables() != _sage_const_2 :
        raise ValueError("pol is not bivariate")

    P = PolynomialRing(ZZ, names=('x', 'y',)); (x, y,) = P._first_ngens(2)
    pol = pol(x,y)

    # Handle case where pol(0,0) == 0
    xoffset = _sage_const_0 

    while pol(xoffset,_sage_const_0 ) == _sage_const_0 :
        xoffset += _sage_const_1 

    pol = pol(x+xoffset,y)

    # Handle case where gcd(pol(0,0),X*Y) != 1
    while gcd(pol(_sage_const_0 ,_sage_const_0 ), X) != _sage_const_1 :
        X = next_prime(X, proof=False)

    while gcd(pol(_sage_const_0 ,_sage_const_0 ), Y) != _sage_const_1 :
        Y = next_prime(Y, proof=False)

    pol = P(pol/gcd(pol.coefficients())) # seems to be helpful
    p00 = pol(_sage_const_0 ,_sage_const_0 )
    delta = max(pol.degree(x),pol.degree(y)) # maximum degree of any variable

    W = max(abs(i) for i in pol(x*X,y*Y).coefficients())
    u = W + ((_sage_const_1 -W) % abs(p00))
    N = u*(X*Y)**k # modulus for polynomials

    # Construct polynomials
    p00inv = inverse_mod(p00,N)
    polq = P(sum((i*p00inv % N)*j for i,j in zip(pol.coefficients(),
                                                 pol.monomials())))
    polynomials = []
    for i in range(delta+k+_sage_const_1 ):
        for j in range(delta+k+_sage_const_1 ):
            if _sage_const_0  <= i <= k and _sage_const_0  <= j <= k:
                polynomials.append(polq * x**i * y**j * X**(k-i) * Y**(k-j))
            else:
                polynomials.append(x**i * y**j * N)

    # Make list of monomials for matrix indices
    monomials = []
    for i in polynomials:
        for j in i.monomials():
            if j not in monomials:
                monomials.append(j)
    monomials.sort()

    # Construct lattice spanned by polynomials with xX and yY
    L = matrix(ZZ,len(monomials))
    for i in range(len(monomials)):
        for j in range(len(monomials)):
            L[i,j] = polynomials[i](X*x,Y*y).monomial_coefficient(monomials[j])

    # makes lattice upper triangular
    # probably not needed, but it makes debug output pretty
    L = matrix(ZZ,sorted(L,reverse=True))

    if debug:
        print("Bitlengths of matrix elements (before reduction):")
        print(L.apply_map(lambda x: x.nbits()).str())

    L = L.LLL()

    if debug:
        print("Bitlengths of matrix elements (after reduction):")
        print(L.apply_map(lambda x: x.nbits()).str())

    roots = []

    for i in range(L.nrows()):
        if debug:
            print("Trying row {}".format(i))

        # i'th row converted to polynomial dividing out X and Y
        pol2 = P(sum(map(mul, zip(L[i],monomials)))(x/X,y/Y))

        r = pol.resultant(pol2, y)

        if r.is_constant(): # not independent
            continue

        for x0, _ in r.univariate_polynomial().roots():
            if x0-xoffset in [i[_sage_const_0 ] for i in roots]:
                continue
            if debug:
                print("Potential x0:",x0)
            for y0, _ in pol(x0,y).univariate_polynomial().roots():
                if debug:
                    print("Potential y0:",y0)
                if (x0-xoffset,y0) not in roots and pol(x0,y0) == _sage_const_0 :
                    roots.append((x0-xoffset,y0))
    return roots

