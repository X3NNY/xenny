def ecb_blasting_attack(N, encrypt):
    s = b'0' * (16*N - 1)
    flag = b''
    for i in range(16*N):
        rec = encrypt(s)[:16*N]
        for j in range(256):
            tmp = b'0' * (16*N - i) + flag + bytes([j])
            res = encrypt(tmp)[:16*N]
            if rec == res:
                flag += bytes([j])
                # print(flag)
                s = s[:-1]
                break
    return flag