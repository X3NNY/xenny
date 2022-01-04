# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      short_pad_attack
   Description :
   Author :         x3nny
   date :           2021/7/23
-------------------------------------------------
   Change Activity:
                    2021/7/23: Init
-------------------------------------------------
"""
__author__ = 'x3nny'


# Franklin-Reiter attack against RSA.
# If two messages differ only by a known fixed difference between the two messages
# and are RSA encrypted under the same RSA modulus N
# then it is possible to recover both of them.

# Inputs are modulus, known difference, ciphertext 1, ciphertext2.
# Ciphertext 1 corresponds to smaller of the two plaintexts. (The one without the fixed difference added to it)
def franklinReiter(n,e,r,c1,c2):
    R.<X> = Zmod(n)[]
    f1 = X^e - c1
    f2 = (X + r)^e - c2
    # coefficient 0 = -m, which is what we wanted!
    return Integer(n-(compositeModulusGCD(f1,f2)).coefficients()[0])

  # GCD is not implemented for rings over composite modulus in Sage
  # so we do our own implementation. Its the exact same as standard GCD, but with
  # the polynomials monic representation
def compositeModulusGCD(a, b):
    if(b == 0):
        return a.monic()
    else:
        return compositeModulusGCD(b, a % b)

def CoppersmithShortPadAttack(e,n,C1,C2,eps=1/30):
    """
    Coppersmith's Shortpad attack!
    Figured out from: https://en.wikipedia.org/wiki/Coppersmith's_attack#Coppersmith.E2.80.99s_short-pad_attack
    """
    import binascii
    P.<x,y> = PolynomialRing(ZZ)
    ZmodN = Zmod(n)
    g1 = x^e - C1
    g2 = (x+y)^e - C2
    res = g1.resultant(g2)
    P.<y> = PolynomialRing(ZmodN)
    # Convert Multivariate Polynomial Ring to Univariate Polynomial Ring
    rres = 0
    for i in range(len(res.coefficients())):
        rres += res.coefficients()[i]*(y^(res.exponents()[i][1]))

    diff = rres.small_roots(epsilon=eps)
    recoveredM1 = franklinReiter(n,e,diff[0],C1,C2)
    print(recoveredM1)
    print("Message is the following hex, but potentially missing some zeroes in the binary from the right end")
    print(hex(recoveredM1))
    print("Message is one of:")
    for i in range(8):
        msg = hex(Integer(recoveredM1*pow(2,i)))
        if(len(msg)%2 == 1):
            msg = '0' + msg
        if(msg[:2]=='0x'):
            msg = msg[:2]
        print(binascii.unhexlify(msg))

def testCoppersmithShortPadAttack(eps=1/25):
    from Crypto.PublicKey import RSA
    import random
    import math
    import binascii
    M = "flag{This_Msg_Is_2_1337}"
    M = int(binascii.hexlify(M),16)
    e = 3
    nBitSize =  8192
    key = RSA.generate(nBitSize)
    #Give a bit of room, otherwhise the epsilon has to be tiny, and small roots will take forever
    m = int(math.floor(nBitSize/(e*e))) - 400
    assert (m < nBitSize - len(bin(M)[2:]))
    r1 = random.randint(1,pow(2,m))
    r2 = random.randint(r1,pow(2,m))
    M1 = pow(2,m)*M + r1
    M2 = pow(2,m)*M + r2
    C1 = Integer(pow(M1,e,key.n))
    C2 = Integer(pow(M2,e,key.n))
    CoppersmithShortPadAttack(e,key.n,C1,C2,eps)


n= 113604829563460357756722229849309932731534576966155520277171862442445354404910882358287832757024693652075211204635679309777620586814014894544893424988818766425089667672311645586528776360047956843961901352792631908859388801090108188344342619580661377758180391734771694803991493164412644148805229529911069578061
e=7


#c1= 112992730284209629010217336632593897028023711212853788739137950706145189880318698604512926758021533447981943498594790549326550460216939216988828130624120379925895123186121819609415184887470233938291227816332249857236198616538782622327476603338806349004620909717360739157545735826670038169284252348037995399308
#c2= 112992730284209629010217336632593897028023711212853788739137950706145189880318698604512926758021552486915464025361447529153776277710423467951041523831865232164370127602772602643378592695459331174613894578701940837730590029577336924367384969935652616989527416027725713616493815764725131271563545176286794438175
c1 = 16404985139084147094704300764850430964980485772400565266054075398380588297033201409914512724255440373095027298869259036450071617770755361938461322132693877590521575670718076480353565935028734363256919872879837455527948173237810119579078252909879868459848240229599708133153841801633280283847680255816123323196
c2 = 92463268823628386526871956385934776043432833035349654252757452728405540022093349560058649691620353528569690982904353035470935543182784600771655097406007508218346417446808306197613168219068573563402315939576563452451487014381380516422829248470476887447827532913133023890886210295009811931573875721299817276803

m = franklinReiter(n,e,1,c1,c2)
from Crypto.Util.number import *
print(long_to_bytes(m))
