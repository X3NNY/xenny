import base64

base16_table = b"0123456789ABCDEF"
base32_table = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567"
base36_table = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
base58_table = b"123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
base62_table = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
base64_table = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
base85_table = b"0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!#$%&()*+-;<=>?@^_`{|}~"
base91_table = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&()*+,./:;<=>?@[]^_`{|}~\""
base92_table = b"!#$%&'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}"


base92_ord = lambda x: 0 if x == ord('!') else x - ord('#') + 1 if ord('#') <= x <= ord('_') else x - ord(
    'a') + 62


def b16encode(content: bytes, code_table: bytes = None):
    cipher = base64.b16encode(content)
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(base64_table, code_table))
    return cipher


def b16decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base64_table))
    return base64.b16decode(cipher)


def b32encode(content: bytes, code_table: bytes = None):
    cipher = base64.b32encode(content)
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(base32_table, code_table))
    return cipher


def b32decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base32_table))
    return base64.b32decode(cipher)


def b36encode(content: bytes, code_table: bytes = None):
    num = 0
    alphabet = base36_table if code_table is None else code_table
    for i in content:
        num = num*256 + i

    value = []
    while num != 0:
        num, index = divmod(num, 36)
        value.append(alphabet[index])

    return bytes(value)[::-1] or b"0"


def b36decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base36_table))
    num = hex(int(cipher, 36))[2:]

    res = ""
    for i in range(len(num) // 2):
        res += chr(int(num[2*i:2*i+2], 16))

    return res.encode()


def b58encode(content: bytes, code_table: bytes = None):
    num = 0
    alphabet = base58_table if code_table is None else code_table
    for i in content:
        num = num * 256 + i

    value = []
    while num != 0:
        num, index = divmod(num, 58)
        value.append(alphabet[index])

    return bytes(value)[::-1] or b"0"


def b58decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base58_table))
    num = 0
    for i in cipher:
        v = base58_table.index(i)
        num = num * 58 + v
    num = hex(num)[2:]

    res = ""
    for i in range(len(num) // 2):
        res += chr(int(num[2*i:2*i+2], 16))

    return res.encode()


def b62encode(content: bytes, code_table: bytes = None):
    num = 0
    alphabet = base62_table if code_table is None else code_table
    for i in content:
        num = num * 256 + i

    value = []
    while num != 0:
        num, index = divmod(num, 62)
        value.append(alphabet[index])

    return bytes(value)[::-1] or b"0"


def b62decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base62_table))
    num = 0
    for i in cipher:
        v = base62_table.index(i)
        num = num * 62 + v
    num = hex(num)[2:]

    res = ""
    for i in range(len(num) // 2):
        res += chr(int(num[2*i:2*i+2], 16))

    return res.encode()


def b64encode(content: bytes, code_table: bytes = None):
    cipher = base64.b64encode(content)
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(base64_table, code_table))
    return cipher


def b64decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base64_table))
    return base64.b64decode(cipher)


def b85encode(content: bytes, code_table: bytes = None):
    cipher = base64.b85encode(content)
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(base85_table, code_table))
    return cipher


def b85decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base85_table))
    return base64.b85decode(cipher)


def b91encode(content: bytes, code_table: bytes = None):
    b = 0
    n = 0
    out = []
    for i in content:
        b |= i << n
        n += 8
        if n > 13:
            v = b & 8191
            if v > 88:
                b >>= 13
                n -= 13
            else:
                v = b & 16383
                b >>= 14
                n -= 14
            out.append(base91_table[v % 91])
            out.append(base91_table[v // 91])
    if n:
        out.append(base91_table[b % 91])
        if n > 7 or b > 90:
            out.append(base91_table[b // 91])

    out = bytes(out)
    if code_table is not None:
        out = out.translate(bytes.maketrans(base91_table, code_table))
    return out


def b91decode(cipher: bytes, code_table: bytes = None):
    if code_table is not None:
        cipher = cipher.translate(bytes.maketrans(code_table, base91_table))
    v = -1
    b = 0
    n = 0
    out = []
    for i in cipher:
        if not i in base91_table:
             continue
        c = base91_table.index(i)
        if v < 0:
            v = c
        else:
            v += c * 91
            b |= v << n
            n += 13 if (v & 8191) > 88 else 14
            while True:
                out.append(b & 255)
                b >>= 8
                n -= 8
                if not n > 7:
                    break
            v = -1
    if v + 1:
        out.append((b | v << n) & 255)
    return bytes(out)


def b92encode(content: bytes, code_table: bytes = None):
    bitstr = ''
    while len(bitstr) < 13 and content:
        bitstr += bin(content[0])[2:].zfill(8)
        content = content[1:]

    res = ""
    while len(bitstr) > 13 or content:
        i = int(bitstr[:13], 2)
        res += chr(base92_table[i // 91])
        res += chr(base92_table[i % 91])
        bitstr = bitstr[13:]
        while len(bitstr) < 13 and content:
            bitstr += bin(content[0])[2:].zfill(8)
            content = content[1:]

    if bitstr:
        if len(bitstr) < 7:
            bitstr += '0' * (6 - len(bitstr))
            res += chr(base92_table[int(bitstr, 2)])
        else:
            bitstr += '0' * (13 - len(bitstr))
            i = int(bitstr, 2)
            res += chr(base92_table[i // 91])
            res += chr(base92_table[i % 91])
    res = res.encode()
    if code_table is not None:
        res = res.maketrans(bytes.translate(base92_table, code_table))
    return res


def b92decode(cipher: bytes, code_table: bytes = None):
    bitstr = ''
    res = ""
    for i in range(len(cipher) // 2):
        x = base92_ord(cipher[2*i]) * 91 + base92_ord(cipher[2*i + 1])
        bitstr += bin(x)[2:].zfill(13)
        while 8 <= len(bitstr):
            res += chr(int(bitstr[:8], 2))
            bitstr = bitstr[8:]

    if len(cipher) % 2 == 1:
        x = base92_ord(cipher[-1])
        bitstr += bin(x)[2:].zfill(6)
        while 8 <= len(bitstr):
            res += chr(int(bitstr[:8], 2))
            bitstr = bitstr[8:]

    res = res.encode()
    if code_table is not None:
        res = res.translate(bytes.maketrans(code_table, base92_table))
    return res


def b128encode(content: bytes, code_table: bytes = None): ...
def b128decode(cipher: bytes, code_table: bytes = None): ...


base16_encode = b16encode
base16_decode = b16decode

base32_encode = b32encode
base32_decode = b32decode

base36_encode = b36encode
base36_decode = b36decode

base58_encode = b58encode
base58_decode = b58decode

base62_encode = b62encode
base62_decode = b62decode

base64_encode = b64encode
base64_decode = b64decode

base85_encode = b85encode
base85_decode = b85decode

base91_encode = b91encode
base91_decode = b91decode

base92_encode = b92encode
base92_decode = b92decode

base128_encode = b128encode
base128_decode = b128decode


# print(base58_encode(b'A')) # 对a进行base64编码
# print(base64_decode(b'ME====')) # 进行base64解码
#
# print(base92_encode(b'a')) # 对a进行base92编码


# print(base64_encode(b'flag{xxxxxxxxx}', b'DEFGHIJmno789+B1Za/STUpqrstKkluv234hijXYwxyzMC0NOP56VWLQRbcdefgA'))

# print(base64_decode(b'sXP3sQCRum3Rum3Rum3f', b'DEFGHIJmno789+B1Za/STUpqrstKkluv234hijXYwxyzMC0NOP56VWLQRbcdefgA'))

# print(base32_encode(b'hello'))
# print(base32_encode(b'hello', b'qwertyuiopasdfghjklzxcvbnm123456'))
# print(base32_decode(b'fwlvn2rh', b'qwertyuiopasdfghjklzxcvbnm123456'))
# print(base32_decode(b'ie======', b"ABCDEFGHIJKLMNOPQRSTUVWXYZ234567".lower()))
print(base92_decode(b'73E-30U1&>V-H965S95]I<U]P;W=E<GT`'))
if __name__ == '__main__':
    pass

