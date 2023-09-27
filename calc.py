import numpy as np
from util import *


def he_add(x1, x2):
    return x1 + x2


def he_sub(x1, x2):
    return x1 - x2


def he_mult(x1, x2):
    lut = create_lut(f_square_by_4)
    tmp1 = x1 + x2
    tmp2 = x1 - x2
    tmp3 = pbs(tmp1, lut)
    tmp4 = pbs(tmp2, lut)
    tmp5 = tmp3 - tmp4
    return tmp5


def he_lut(x, f):
    lut = create_lut(f)
    tmp1 = pbs(x, lut)
    return tmp1


def he_add_1d(x1, x2):
    assert len(x1) == len(x2)
    res = []
    for i in range(len(x1)):
        res.append(he_add(x1[i], x2[i]))
    return res


def he_sub_1d(x1, x2):
    assert len(x1) == len(x2)
    res = []
    for i in range(len(x1)):
        res.append(he_sub(x1[i], x2[i]))
    return res


def he_mult_1d(x1, x2):
    assert len(x1) == len(x2)
    res = []
    for i in range(len(x1)):
        res.append(he_mult(x1[i], x2[i]))
    return res


def he_sum_all_1d(x):
    res = x[0]
    for i in range(1, len(x)):
        res = he_add(res, x[i])
    return res


def he_inner(x1, x2):
    assert len(x1) == len(x2)
    res = []
    for i in range(len(x1)):
        res.append(he_mult(x1[i], x2[i]))
    return he_sum_all_1d(res)


def he_lut_1d(x, f):
    res = []
    for i in range(len(x)):
        res.append(he_lut(x[i], f))
    return res


def he_matrix_vector_dot(m, x):
    # m = (dout, din)
    # x = (din)
    assert len(m[0]) == len(x)
    res = []
    for i in range(len(m)):
        res.append(he_inner(m[i], x))
    return res


def he_matrix_matrix_dot(m1, m2):
    # m1 = (d1, k)
    # m2 = (k, d2)
    assert len(m1[0]) == len(m2)
    res = []
    for i in range(len(m2[0])):
        res.append(he_matrix_vector_dot(m1, m2[:][i]))
    return res
