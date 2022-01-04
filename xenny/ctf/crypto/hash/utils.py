from hashlib import md5, sha256, sha1
import re
from itertools import product
from string import ascii_letters, digits

default_alphabet = list(ascii_letters + digits)

def proof_of_work(known, cipher, encrypt, alphabet=None):
    """
    ctf中常见的的hash工作量证明，known是hex数据，未知量使用xx代替，例如31xx32xx代表1?2?
    :param known:
    :param cipher:
    :param encrypt: hashlib.md5, sha1, sha256 etc...
    :return:
    """
    if alphabet is None:
        alphabet = default_alphabet
    known = known.lower().split('xx')
    for i in range(len(known)):
        known[i] = bytes.fromhex(known[i])
    # print(known)
    for v in product(alphabet, repeat=len(known)-1):
        tmp = known[0]
        for i in range(len(v)):
            tmp += v[i].encode() + known[i+1]
        # print(tmp)
        print(len(encrypt(encrypt(tmp).digest()).hexdigest()))
        if encrypt(encrypt(tmp).digest()).hexdigest() == cipher:
            return v, tmp

if __name__ == '__main__':
    s = 'd1faec9480b4e6d619aa0061b04827f3d5af1c2c'
    print(hex(int.from_bytes(proof_of_work('df9a936bb8dd93xxxxxx', s, sha1, [chr(_) for _ in range(256)])[1], 'big')))