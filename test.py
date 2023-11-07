import random
import numpy as np
import pytest
from constants import *
import constants
from util import *
from calc import *
import math
import functools


def get_random_x():
    tmp1 = random.random()
    tmp2 = tmp1 * (b-a) + a
    return tmp2


def test_encode_decode():
    for _ in range(test_N):
        tmp1 = get_random_x()
        e1 = encode_a_b(tmp1)
        d1 = decode_a_b(e1)
        assert math.isclose(tmp1, d1, rel_tol=tolerance)


def test_sum():
    for _ in range(test_N):
        x1 = get_random_x()
        x2 = get_random_x()
        e1 = encode_a_b(x1)
        e2 = encode_a_b(x2)
        e_add = e1 + e2
        ans = x1 + x2
        d = decode_a_b(e_add)
        print(f"and: {ans}")
        print(f"dec: {d}")
        if (ans < a) or (ans > b):
            assert True
        else:
            assert math.isclose(d, ans, rel_tol=tolerance)


def test_sub():
    for _ in range(test_N):
        x1 = get_random_x()
        x2 = get_random_x()
        e1 = encode_a_b(x1)
        e2 = encode_a_b(x2)
        e_sub = e1 - e2
        ans = x1 - x2
        d = decode_a_b(e_sub)
        print(f"and: {ans}")
        print(f"dec: {d}")
        if (ans < a) or (ans > b):
            assert True
        else:
            assert math.isclose(d, ans, rel_tol=tolerance)


def test_identity_pbs():
    for _ in range(test_N):
        lut = create_lut(f_identity)
        x = get_random_x()
        e1 = encode_a_b(x)
        tmp1 = pbs(e1, lut)
        tmp2 = decode_a_b(tmp1)
        flag1 = math.isclose(tmp2, f_identity(x), rel_tol=tolerance)
        flag2 = math.isclose(tmp2, f_identity(x), abs_tol=abs_tol)
        assert flag1 or flag2

def test_scalar_add_pbs():
    for _ in range(test_N):
        s = random.random()
        lut = create_lut(functools.partial(f_scalar_add, a=s))
        x = get_random_x()
        e1 = encode_a_b(x)
        tmp1 = pbs(e1, lut)
        tmp2 = decode_a_b(tmp1)

        ans = f_scalar_add(x, s)
        if ans < constants.a or ans > constants.b:
          assert True
          continue
        
        #print(f"ans: {ans}")
        #print(f"dec: {tmp2}")
        flag1 = math.isclose(tmp2, ans, rel_tol=tolerance)
        flag2 = math.isclose(tmp2, ans, abs_tol=abs_tol)
        assert flag1 or flag2

def test_scalar_sub_pbs():
    for _ in range(test_N):
        s = random.random()
        lut = create_lut(functools.partial(f_scalar_sub, a=s))
        x = get_random_x()
        e1 = encode_a_b(x)
        tmp1 = pbs(e1, lut)
        tmp2 = decode_a_b(tmp1)

        ans = f_scalar_sub(x, s)
        if ans < constants.a or ans > constants.b:
          assert True
          continue
        
        #print(f"ans: {ans}")
        #print(f"dec: {tmp2}")
        flag1 = math.isclose(tmp2, ans, rel_tol=tolerance)
        flag2 = math.isclose(tmp2, ans, abs_tol=abs_tol)
        assert flag1 or flag2

def test_scalar_mult_pbs():
    for _ in range(test_N):
        s = random.random()
        lut = create_lut(functools.partial(f_scalar_mult, a=s))
        x = get_random_x()
        e1 = encode_a_b(x)
        tmp1 = pbs(e1, lut)
        tmp2 = decode_a_b(tmp1)

        ans = f_scalar_mult(x, s)
        if ans < constants.a or ans > constants.b:
          assert True
          continue
        
        #print(f"ans: {ans}")
        #print(f"dec: {tmp2}")
        flag1 = math.isclose(tmp2, ans, rel_tol=tolerance)
        flag2 = math.isclose(tmp2, ans, abs_tol=abs_tol)
        assert flag1 or flag2

def test_scalar_div_pbs():
    for _ in range(test_N):
        s = random.random()
        lut = create_lut(functools.partial(f_scalar_div, a=s))
        x = get_random_x()
        e1 = encode_a_b(x)
        tmp1 = pbs(e1, lut)
        tmp2 = decode_a_b(tmp1)

        ans = f_scalar_div(x, s)
        if ans < constants.a or ans > constants.b:
          assert True
          continue
        
        #print(f"ans: {ans}")
        #print(f"dec: {tmp2}")
        flag1 = math.isclose(tmp2, ans, rel_tol=tolerance)
        flag2 = math.isclose(tmp2, ans, abs_tol=abs_tol)
        assert flag1 or flag2

def test_uint8_encode_decode():
    for _ in range(test_N):
        x = random.randint(0, (1 << 32) - 1)
        tmp = int32_to_uint8_array(x)
        tmp2 = uint8_array_to_int32(tmp)
        assert x == tmp2

def test_square_div_4_pbs():
    for _ in range(test_N):
        lut = create_lut(functools.partial(f_square_by_4))
        x = get_random_x() / pow(2, 2)
        e1 = encode_a_b(x)
        tmp1 = pbs(e1, lut)
        tmp2 = decode_a_b(tmp1)

        ans = f_square_by_4(x)
        if ans < constants.a or ans > constants.b:
          assert True
          continue
        
        #print(f"ans: {ans}")
        #print(f"dec: {tmp2}")
        flag1 = math.isclose(tmp2, ans, rel_tol=tolerance)
        flag2 = math.isclose(tmp2, ans, abs_tol=abs_tol)
        assert flag1 or flag2


def test_mult():
    for _ in range(test_N):
        lut = create_lut(f_square_by_4)
        x1 = get_random_x() / pow(2, 2)
        x2 = get_random_x() / pow(2, 2)
        if (x1*x2 >= b) or (x1*x2 <= a):
            assert True
        else:
            e1 = encode_a_b(x1)
            e2 = encode_a_b(x2)
            tmp1 = e1 + e2
            tmp2 = e1 - e2
            tmp3 = pbs(tmp1, lut)
            tmp4 = pbs(tmp2, lut)
            tmp5 = tmp3 - tmp4
            tmp6 = decode_a_b(tmp5)
            ans = x1 * x2

            print(f"(x1, x2): ({x1}, {x2})")
            print(f"ans: {ans}")
            print(f"dec: {tmp6}")
            flag1 = math.isclose(tmp6, ans, rel_tol=tolerance)
            flag2 = math.isclose(tmp6, ans, abs_tol=abs_tol)
            assert flag1 or flag2

if __name__ == "__main__":
  print("hello, world")
  #test_scalar_add_pbs()
#   test_square_div_4_pbs()
#   print("\nokay===")
  test_mult()
