def rc4(key, content):
    key_len = len(key)
    S = [i for i in range(256)]
    T = [key[i % key_len] for i in range(256)]

    j = 0
    for i in range(256):
        j = (j + S[i] + T[i]) % 256
        S[i], S[j] = S[j], S[i]

    i = j = 0
    res = []
    for c in content:
        i = (i+1) % 256
        j = (j+S[i]) % 256
        S[i], S[j] = S[j], S[i]
        t = (S[i] + S[j]) % 256
        res.append(c ^ t)
    return bytes(res)