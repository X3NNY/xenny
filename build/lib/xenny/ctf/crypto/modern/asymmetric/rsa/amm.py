from gmpy2 import *
from Crypto.Util.number import *
import random
import math

def onemod(e, q):
    p = random.randint(1, q-1)
    while(powmod(p, (q-1)//e, q) == 1):  # (r,s)=1
        p = random.randint(1, q)
    return p


def AMM_rth(o, r, q):  # r|(q-1)
    """
    x^r % q = o
    :param o:
    :param r:
    :param q:
    :return:
    """
    assert((q-1) % r == 0)
    p = onemod(r, q)

    t = 0
    s = q-1
    while(s % r == 0):
        s = s//r
        t += 1
    k = 1
    while((s*k+1) % r != 0):
        k += 1
    alp = (s*k+1)//r

    a = powmod(p, r**(t-1)*s, q)
    b = powmod(o, r*a-1, q)
    c = powmod(p, s, q)
    h = 1

    for i in range(1, t-1):
        d = powmod(int(b), r**(t-1-i), q)
        if d == 1:
            j = 0
        else:
            j = (-int(math.log(d, a))) % r
        b = (b*(c**(r*j))) % q
        h = (h*c**j) % q
        c = (c*r) % q
    result = (powmod(o, alp, q)*h)
    return result


def ALL_Solution(m, q, rt, cq, e):
    mp = []
    for pr in rt:
        r = (pr*m) % q
        # assert(pow(r, e, q) == cq)
        mp.append(r)
    return mp


def ALL_ROOT2(r, q):  # use function set() and .add() ensure that the generated elements are not repeated
    li = set()
    while(len(li) < r):
        p = powmod(random.randint(1, q-1), (q-1)//r, q)
        li.add(p)
    return li


def attack(p, q, e, check=None):
    cp = c % p
    cq = c % q

    mp = AMM_rth(cp, e, p)
    mq = AMM_rth(cq, e, q)

    rt1 = ALL_ROOT2(e, p)
    rt2 = ALL_ROOT2(e, q)

    amp = ALL_Solution(mp, p, rt1, cp, e)
    amq = ALL_Solution(mq, q, rt2, cq, e)

    if check is not None:
        j = 1
        t1 = invert(q, p)
        t2 = invert(p, q)
        for mp1 in amp:
            for mq1 in amq:
                j += 1
                if j % 1000000 == 0:
                    print(j)
                ans = (mp1 * t1 * q + mq1 * t2 * p) % (p * q)
                if check(ans):
                    return ans
    return amp, amq

if __name__ == '__main__':
    c = 10562302690541901187975815594605242014385201583329309191736952454310803387032252007244962585846519762051885640856082157060593829013572592812958261432327975138581784360302599265408134332094134880789013207382277849503344042487389850373487656200657856862096900860792273206447552132458430989534820256156021128891296387414689693952047302604774923411425863612316726417214819110981605912408620996068520823370069362751149060142640529571400977787330956486849449005402750224992048562898004309319577192693315658275912449198365737965570035264841782399978307388920681068646219895287752359564029778568376881425070363592696751183359
    p = 199138677823743837339927520157607820029746574557746549094921488292877226509198315016018919385259781238148402833316033634968163276198999279327827901879426429664674358844084491830543271625147280950273934405879341438429171453002453838897458102128836690385604150324972907981960626767679153125735677417397078196059
    q = 112213695905472142415221444515326532320352429478341683352811183503269676555434601229013679319423878238944956830244386653674413411658696751173844443394608246716053086226910581400528167848306119179879115809778793093611381764939789057524575349501163689452810148280625226541609383166347879832134495444706697124741
    e = 0x1337
    cp = c % p
    cq = c % q

    mp = AMM_rth(cp, e, p)
    mq = AMM_rth(cq, e, q)

    rt1 = ALL_ROOT2(e, p)
    rt2 = ALL_ROOT2(e, q)

    amp = ALL_Solution(mp, p, rt1, cp, e)
    amq = ALL_Solution(mq, q, rt2, cq, e)

    attack(amp, amq, e, p, q)