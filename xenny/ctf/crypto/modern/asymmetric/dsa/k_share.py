import gmpy2


def attack(r, s1, s2, hm1, hm2, q):
    k = (hm1-hm2)*gmpy2.invert(s1-s2,q)%q
    x = gmpy2.invert(r,q)*(k*s1-hm1)%q
    return k, x






s3 = 0x30EB88E6A4BFB1B16728A974210AE4E41B42677D
s4 = 0x5E10DED084203CCBCEC3356A2CA02FF318FD4123
r = 0x5090DA81FEDE048D706D80E0AC47701E5A9EF1CC
h3 = 1104884177962524221174509726811256177146235961550
h4 = 943735132044536149000710760545778628181961840230
q = 768204286206312924745826772404361572053995803069

k, x = attack(r, s3, s4, h3, h4, q)
print(x)