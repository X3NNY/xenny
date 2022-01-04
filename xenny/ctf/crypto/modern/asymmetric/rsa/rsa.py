from typing import List

from Crypto.Util.number import long_to_bytes
import logging

from gmpy2 import powmod, invert

from ctf.crypto.modern.asymmetric.rsa import small_plain, wiener, schemidt_samoa, williams_pp1, pollard_p_1, ex_wiener
from ctf.crypto.modern.asymmetric.rsa import dpleak
from util.utils import is_sage

ATTACKS = [
    'dpdqleak',
    'dpleak',
    'small_plain',
    'wiener',
    'schemidt_samoa',
    'williams_pp1',
    'pollard_p_1',
    'ex_wiener',
    'factordb',
    'amm',
    'same_module',
    'lowe_broadcast',
    'rabin'
]
SAGE_ATTACKS = set('ex_wiener')


class key:
    def __init__(self,
                 n=None,
                 e=None,
                 d=None,
                 p=None,
                 q=None,
                 dp=None,
                 dq=None,
                 phi=None,
                 u=None,
                 m=None,
                 c=None):
        self.n = n
        self.e = e
        self.d = d
        self.p = p
        self.q = q
        self.dp = dp
        self.dq = dq
        self.phi = phi
        self.u = u
        self.m = [m]
        self.c = c

    @staticmethod
    def from_pem(pem): ...

    @staticmethod
    def from_der(der): ...


class RSA:
    timout_seconds = 60

    def __init__(self, keys, timeout=60):
        self.logger = logging.getLogger("global_logger")
        if isinstance(keys, list):
            self.keys = keys
        elif isinstance(keys, key):
            self.keys = [key]
        else:
            raise Exception("argument must be a list or a key object, not '{}'".format(keys.__class__.__name__))

        self.timout_seconds = timeout

    def print_m(self):
        for key in self.keys:
            if key.m is not None:
                for m in key.m:
                    print(long_to_bytes(m))

    def get_m(self):
        res = []
        for key in self.keys:
            if key.m is not None:
                res.append(key.m)
        return res

    def attack(self, attacks=None):
        """
        attacks:
            'dpdqleak',
            'dpleak',
            'small_plain',
            'wiener',
            'schemidt_samoa',
            'williams_pp1',
            'pollard_p_1',
            'ex_wiener',
            'factordb',
            'amm',
        :param attacks:
        :return:
        """
        if attacks is None:
            attacks = ATTACKS
        if isinstance(attacks, str):
            attacks = [attacks]

        for attack in attacks:
            try:
                if attack in SAGE_ATTACKS:
                    if not is_sage():
                        self.logger.warning(
                            "[!] Can't load %s because sage is not installed" % attack
                        )
                        continue
                self.logger.info(
                    "[*] Performing %s attack." % attack
                )
                self.__getattribute__(attack + '_attack')()
            except IndentationError:
                raise IndentationError("no attack '{}'".format(attack))
            except Exception:
                pass

    def dpdqleak_attack(self):
        for key in self.keys:
            if key.dp is not None and \
                    key.dq is not None and \
                    key.q is not None and \
                    key.p is not None and \
                    key.c is not None:
                try:
                    res = dpleak.dpdqleak(key.dp, key.dq, key.p, key.q, key.c)
                    key.m.append(res)
                except Exception:
                    pass

    def dpleak_attack(self):
        for key in self.keys:
            if key.e is not None and \
                    key.dp is not None and \
                    key.n is not None and \
                    key.c is not None:
                try:
                    key.m.append(dpleak.dpdqleak(key.e, key.dp, key.n.key.c, self.timout_seconds))
                except Exception:
                    pass

    def small_plain_attack(self):
        for key in self.keys:
            if key.e is not None and \
                    key.c is not None:
                key.m.append(small_plain.attack(key.e, key.c))

    def wiener_attack(self):
        for key in self.keys:
            if key.e is not None and \
                    key.n is not None:
                d, p, q = wiener.attack(key.n, key.e)
                if d is not None:
                    key.d = d
                    key.p = p
                    key.q = q
                    if key.c is not None:
                        key.m.append(powmod(key.c, d, key.n))
                    # self.logger("[+] Find d: %d" % d)

    def schemidt_samoa_attack(self):
        for key in self.keys:
            if key.n is not None and \
                    key.d is not None and \
                    key.c is not None:
                key.m.append(schemidt_samoa.attack(key.n, key.d, key.c))

    def williams_pp1_attack(self):
        for key in self.keys:
            if key.n is not None:
                p, q = williams_pp1.attack(key.n, timeout=self.timout_seconds)
                if p is not None:
                    key.p = p
                    key.q = q
                    if key.c is not None and key.e is not None:
                        key.m.append(powmod(key.c, invert(key.e, (key.p-1)*(key.q-1)), key.n))


    def pollard_p_1_attack(self):
        for key in self.keys:
            if key.n is not None:
                p, q = pollard_p_1.attack(key.n, timeout=self.timout_seconds)
                if p is not None:
                    key.p = p
                    key.q = q
                    if key.c is not None and key.e is not None:
                        key.m.append(powmod(key.c, invert(key.e, (key.p - 1) * (key.q - 1)), key.n))


    def ex_wiener_attack(self):
        for key1 in self.keys:
            for key2 in self.keys:
                if key1.e != key2.e and \
                    key1.e != None and \
                    key2.e != None and \
                    key1.n == key2.n and \
                    key1.n != None:
                    p,q = ex_wiener.attack(key1.n, key1.e, key2.e)
                    if p is not None:
                        key1.p = key2.p = p
                        key2.q = key2.q = q
                        if key1.c is not None:
                            key1.m.append(powmod(key1.c, invert(key1.e, (key1.p - 1) * (key1.q - 1)), key1.n))
                        if key2.c is not None:
                            key2.m.append(powmod(key2.c, invert(key2.e, (key2.p - 1) * (key2.q - 1)), key2.n))

    def factordb_attack(self):
        ...

    def amm_attack(self):
        ...

    def same_module_attack(self):
        ...

    def lowe_broadcast_attack(self):
        ...

    def rabin_attack(self):
        ...


class test:
    def a(self):
        try:
            self.__getattribute__('c')
        except AttributeError:
            raise AttributeError("no attack '{}'".format('123'))

    def b(self, a):
        print(a + 1)


if __name__ == '__main__':
    test().a()
