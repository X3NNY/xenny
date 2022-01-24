# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name :      broadcast_attack_with_linear_padding.sage
   Description :
   Author :         x3nny
   date :           2021/7/14
-------------------------------------------------
   Change Activity:
                    2021/7/14: Init
-------------------------------------------------
"""
__author__ = 'x3nny'

# coding:utf-8
x_calc = lambda x, n: ((n-x)//x+1, (n-x)%x)


def x_change(e_list):
   e_list = [(i, e_list[i]) for i in range(len(e_list))]
   e_list = sorted(e_list, key=lambda x:x[1])
   sum = max_i = 0
   indexs = []
   exponents = []
   for index, exp in e_list:
      sum += 1/exp
      indexs.append(index)
      if exp > max_i:
         max_i = exp
      if sum > 1.:
         break
   for i in range(len(indexs)):
      exponents.append(x_calc(e_list[i][1], max_i))
   return indexs, exponents


def hastad_attack(c_list, n_list, a_list, b_list, e, bits=1000, beta=7./8):
   PR.<x> = PolynomialRing(ZZ)
   f_list = []
   for i in range(len(c_list)):
      f = PR((a_list[i]*x + b_list[i])^e - c_list[i])
      ff = f.change_ring(Zmod(n_list[i]))
      ff = ff.monic()
      f = ff.change_ring(ZZ)
      f_list.append(f)

   F = crt(f_list, n_list)
   M = reduce(lambda x, y: x * y, n_list)
   FF = F.change_ring(Zmod(M))
   m = FF.small_roots(X=2^bits, beta=beta)
   if m:
      return m[0]
   return None


def smupe(c_list, n_list, a_list, b_list, e_list, bits=1000, beta=7./8):
   PR.<x> = PolynomialRing(ZZ)
   f_list = []
   indexs, exponents = x_change(e_list)
   for i in indexs:
      f =  PR((a_list[i]*x + b_list[i])^e_list[i] - c_list[i] )
      ff = f.change_ring(Zmod(n_list[i]))
      ff = ff.monic()
      f = ff.change_ring(ZZ)
      f_list.append(f)
   F = crt([(f_list[i]^exponents[i][0]) * (x^exponents[i][1]) for i in range(len(exponents))], [n_list[i] for i in indexs])

   M = reduce(lambda x, y: x * y, [n_list[i] for i in indexs])
   FF = F.change_ring(Zmod(M))
   m = FF.small_roots(X=2^bits, beta=beta)
   if m:
      return m[0]
   return None


def attack(c_list, n_list, a_list, b_list, e=None, e_list=None, bits=1000, beta=7./8):
   if e is not None:
      return hastad_attack(c_list, n_list, a_list, b_list, e, bits, beta)
   elif e_list is not None:
      return smupe(c_list, n_list, a_list, b_list, e_list, bits, beta)
   return None
