#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import gmpy2
import requests


def attack(n, e, cipher=[]):
    url_1 = "http://factordb.com/index.php?query=%i"
    url_2 = "http://factordb.com/index.php?id=%s"
    s = requests.Session()
    r = s.get(url_1 % n, verify=False)
    regex = re.compile(r"index\.php\?id\=([0-9]+)", re.IGNORECASE)
    ids = regex.findall(r.text)

    # check if only 1 factor is returned
    if len(ids) == 2:
        # theres a chance that the only factor returned is prime, and so we can derive the priv key from it
        regex = re.compile(r"<td>P<\/td>")
        prime = regex.findall(r.text)
        if len(prime) == 1:
            # n is prime, so lets get the key from it
            d = gmpy2.invert(e, n - 1)
            # construct key using only n and d
            priv_key = PrivateKey(e=int(publickey.e), n=int(publickey.n), d=d)
            return (priv_key, None)

    elif len(ids) == 3:
        try:
            regex = re.compile(r'value="([0-9\^\-]+)"', re.IGNORECASE)
            p_id = ids[1]
            r_1 = s.get(url_2 % p_id, verify=False)
            key_p = regex.findall(r_1.text)[0]
            publickey.p = int(key_p) if key_p.isdigit() else solveforp(key_p)

            q_id = ids[2]
            r_2 = s.get(url_2 % q_id, verify=False)
            key_q = regex.findall(r_2.text)[0]
            publickey.q = int(key_q) if key_q.isdigit() else solveforp(key_q)

            if publickey.n != int(publickey.p) * int(publickey.q):
                return (None, None)

        except IndexError:
            return (None, None)

        try:
            priv_key = PrivateKey(
                p=int(publickey.p),
                q=int(publickey.q),
                e=int(publickey.e),
                n=int(publickey.n),
            )
        except ValueError:
            return (None, None)

        return (priv_key, None)
    elif len(ids) > 3:
        phi = 1
        for p in ids[1:]:
            phi *= int(p) - 1
        d = invmod(publickey.e, phi)
        plains = []
        for c in cipher:
            int_big = int.from_bytes(c, "big")
            plain1 = pow(int_big, d, publickey.n)
            plains.append(long_to_bytes(plain1))
        return (None, plains)

if __name__ == '__main__':
    print(attack())
