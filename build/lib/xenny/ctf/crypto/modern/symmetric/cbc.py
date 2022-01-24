from pwn import *

bytesxor = lambda a, b: bytes(i ^ j for i, j in zip(a, b))


def get_last_bit(known, cipher, IV, encrypt):
    """known: first 15 bytes that we know
    cipher: Ek(known+?) where ? is one byte that we want to get returns(?,IV)
    """
    for i in range(256):
        rec = encrypt(bytesxor(IV, known + bytes([i])))  # Ek(known+i) where len(known)=15,len(i)=1
        IV = rec[-16:]
        if rec[:16] == cipher:
            return bytes([i]), IV
    return None


def cbc_blasting_attack(N, IV, encrypt):
    """
    :param N:
    :param IV:
    :param encrypt: (s: bytes) -> bytes
    :return:
    """
    flag = b""
    for k in range(N):
        # k=0:secret[0:15]l={15,14,...,1}
        # k=1:secret[15:31]l={16,15,...,1}
        # k=2:secret[31:47]l={16,15,...,1}
        # k=3:secret[47:48]l={16}
        start = 15 if k == 0 else 16
        end = 15 if k == N - 1 else 0
        for l in range(start, end, -1):
            rec = encrypt(IV[:l])
            if k == 0:
                s = b"\x00" * l + bytesxor(IV[l:-1], flag)
                last_byte = IV[-1:]
                cipher, IV = rec[:16], rec[-16:]
            else:
                kIV, cipher, IV = rec[16 * (k - 1):16 * k], rec[16 * k:16 * (k + 1)], rec[-16:]
                s = xor(kIV, flag[-15:])
                last_byte = kIV[-1:]
            byte, IV = get_last_bit(s, cipher, IV, encrypt)
            flag += bytesxor(byte, last_byte)
            # print(flag.hex(),len(flag))
    return flag
