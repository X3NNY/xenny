# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      smart_attack
   Description :
   Author :         x3nny
   date :           2021/10/7
-------------------------------------------------
   Change Activity:
                    2021/10/7: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

def smart_attack(P,Q,p):
    E = P.curve()
    Eqp = EllipticCurve(Qp(p, 2), [ ZZ(t) + randint(0,p)*p for t in E.a_invariants() ])

    P_Qps = Eqp.lift_x(ZZ(P.xy()[0]), all=True)
    for P_Qp in P_Qps:
        if GF(p)(P_Qp.xy()[1]) == P.xy()[1]:
            break

    Q_Qps = Eqp.lift_x(ZZ(Q.xy()[0]), all=True)
    for Q_Qp in Q_Qps:
        if GF(p)(Q_Qp.xy()[1]) == Q.xy()[1]:
            break

    p_times_P = p*P_Qp
    p_times_Q = p*Q_Qp

    x_P,y_P = p_times_P.xy()
    x_Q,y_Q = p_times_Q.xy()

    phi_P = -(x_P/y_P)
    phi_Q = -(x_Q/y_Q)
    k = phi_Q/phi_P
    return ZZ(k)


def attack(a, b, n, p, q):
    E = EllipticCurve(GF(n),[a,b])
    P = E.point(p)
    Q = E.point(q)
    m = smart_attack(P, Q, n)
    return m


if __name__ == "__main__":
    p = 0xd3ceec4c84af8fa5f3e9af91e00cabacaaaecec3da619400e29a25abececfdc9bd678e2708a58acb1bd15370acc39c596807dab6229dca11fd3a217510258d1b
    A = 0x95fc77eb3119991a0022168c83eee7178e6c3eeaf75e0fdf1853b8ef4cb97a9058c271ee193b8b27938a07052f918c35eccb027b0b168b4e2566b247b91dc07
    B = 0x926b0e42376d112ca971569a8d3b3eda12172dfb4929aea13da7f10fb81f3b96bf1e28b4a396a1fcf38d80b463582e45d06a548e0dc0d567fc668bd119c346b2
    P = (10121571443191913072732572831490534620810835306892634555532657696255506898960536955568544782337611042739846570602400973952350443413585203452769205144937861 , 8425218582467077730409837945083571362745388328043930511865174847436798990397124804357982565055918658197831123970115905304092351218676660067914209199149610)
    Q = (964864009142237137341389653756165935542611153576641370639729304570649749004810980672415306977194223081235401355646820597987366171212332294914445469010927 , 5162185780511783278449342529269970453734248460302908455520831950343371147566682530583160574217543701164101226640565768860451999819324219344705421407572537)

    m = attack(A, B, p, P, Q)
    from Crypto.Util.number import long_to_bytes
    print(long_to_bytes(m))
