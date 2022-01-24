# -*- coding: utf-8 -*-

import re
import requests


def solveforp(equation):
    """
        Parse factordb response
    """
    if "^" in equation:
        k, j = equation.split("^")
    if "-" in j:
        j, sub = j.split("-")
    eq = list(map(int, [k, j, sub]))
    return pow(eq[0], eq[1]) - eq[2]


def attack(n):
    """
        return a prime list of None
    """
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
            return [n]
    elif len(ids) == 3:
        try:
            regex = re.compile(r'value="([0-9\^\-]+)"', re.IGNORECASE)
            p_id = ids[1]
            r_1 = s.get(url_2 % p_id, verify=False)
            key_p = regex.findall(r_1.text)[0]
            p = int(key_p) if key_p.isdigit() else solveforp(key_p)

            q_id = ids[2]
            r_2 = s.get(url_2 % q_id, verify=False)
            key_q = regex.findall(r_2.text)[0]
            q = int(key_q) if key_q.isdigit() else solveforp(key_q)

            if n != int(p) * int(q):
                return None

        except IndexError:
            return None

        return [p, q]
    elif len(ids) > 3:
        regex = re.compile(r'value="([0-9\^\-]+)"', re.IGNORECASE)
        pl = []
        for p in ids[1:]:
            r = s.get(url_2 % p, verify=False)
            key_p = regex.findall(r.text)[0]
            p = int(key_p) if key_p.isdigit() else solveforp(key_p)
            pl.append(p)
        return pl

if __name__ == '__main__':
    print(attack(980710843783426929436352108445477207723530613536846588304753445659989738992892689598648497))
