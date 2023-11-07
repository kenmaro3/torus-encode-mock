import numpy as np
from constants import *


def int32_to_uint8_array(x):
    res = []
    for i in range(4):
        tmp = x >> ((4-i-1) * 8)
        res.append(tmp & ((1 << 8) - 1))
    return res


def uint8_array_to_int32(x):
    res = x[3]
    for i in range(1, 4):
        res += x[3-i] << (i * 8)
    return res


def encode(x):
    #assert x < (1 << clear_text_bit)-1, f"x: {x} !< {(1 << clear_text_bit)-1}"
    if (x >= (1 << clear_text_bit)-1):
        x = 0
    tmp1 = x * pow(2, noise_bit)
    tmp1 = tmp1 * pow(2, (prg_bit - clear_text_bit - noise_bit))
    tmp1 = int(tmp1)
    tmp2 = tmp1 - int(1 << (prg_bit-1))  # shift
    # tmp2 = tmp1
    return tmp2


def decode(x):
    assert x < (1 << prg_bit) - 1, f"{x}, {(1<<prg_bit) - 1}"
    tmp1 = x + int(1 << (prg_bit-1))  # shift back
    #tmp1 = x
    tmp1 = tmp1 / pow(2, noise_bit)
    tmp1 = tmp1 / pow(2, (prg_bit - clear_text_bit - noise_bit))
    return tmp1


def encode_a_b(x):
    tmp1 = (x-a)/(b-a)  # torus
    tmp2 = tmp1 * (1 << clear_text_bit)  # descritised torus
    return encode(tmp2)


def decode_a_b(x):
    tmp1 = decode(x)
    tmp2 = tmp1 / (1 << clear_text_bit)
    tmp3 = tmp2 * (b-a) + a
    return tmp3


def rescale_encoded_value_to_N(x):
    #assert x < (1 << prg_bit) - 1, f"x: {x} !< {(1<<prg_bit) - 1}"
    if (x >= (1 << prg_bit) - 1):
        return 0
    # tmp1 = decode(x)  # descritized by clear_text_bit
    tmp1 = x + int(1 << (prg_bit-1))  # shift back
    tmp1 = tmp1 / pow(2, prg_bit)  # torus
    tmp2 = tmp1 * pow(2, N_bit)
    return int(tmp2)


def inverse_rescale_encoded_value_to_N(x):
    assert x < (1 << N_bit) - 1
    # tmp1 = decode(x)  # descritized by clear_text_bit
    tmp1 = x / pow(2, N_bit)  # torus
    tmp2 = tmp1 * pow(2, prg_bit)
    return int(tmp2)


def pbs(x, lut):
    assert len(lut) == (1 << N_bit)
    tmp1 = rescale_encoded_value_to_N(x)
    return lut[tmp1]


def create_lut(f):
    tmp1 = np.linspace(a, b, 1 << N_bit)
    tmp2 = np.array([f(el) for el in tmp1])
    tmp3 = [encode_a_b(el) for el in tmp2]
    return tmp3


def f_identity(x):
    return x

def f_scalar_add(x, a):
    return x + a

def f_scalar_sub(x, a):
    return x - a

def f_scalar_mult(x, a):
    return x * a

def f_scalar_div(x, a):
    return x / a

def f_relu(x):
    if x > 0:
        return x
    else:
        return 0


def f_square_by_4(x):
    tmp = pow(x, 2) / 4.0
    if (tmp < a) or (tmp > b):
        return 0
    else:
        return tmp


def uint8_array_to_file(x, file_name):
    # Open a text file for writing
    with open(file_name, 'w') as file:
        # Use a for loop to write each element of the list to the file
        for item in x:
            file.write(f"{item},")


def lut_to_uint8_array(x):
    res = []
    for el in x:
        res.append(int32_to_uint8_array(el))
    res = np.array(res)
    res = res.reshape(-1)
    res = list(res)
    assert len(res) == (1 << N_bit)*4
    return res


if __name__ == "__main__":
    # x = 3
    # print(f"x: {x}")
    # e1 = encode_a_b(x)
    # d1 = decode_a_b(e1)
    # print(f"e1: {e1}")
    # print(f"d1: {d1}")
    # tmp1 = rescale_encoded_value_to_N(e1)
    # tmp2 = inverse_rescale_encoded_value_to_N(tmp1)
    # print(f"tmp1: {tmp1}")
    # print(f"tmp2: {tmp2}")
    # d1 = decode_a_b(tmp2)
    # print(f"d1: {d1}")

    # lut = create_lut(f_square_by_4)
    # # print(lut)
    # tmp3 = pbs(e1, lut)
    # d1 = decode_a_b(tmp3)
    # print(f"d1: {d1}")
    # ans = f_square_by_4(x)

    # print(f"ans: {ans}")
    import random

    def get_random_x():
        tmp1 = random.random()
        tmp2 = tmp1 * (b-a) + a
        return tmp2

    lut = create_lut(f_square_by_4)
    tmp = lut_to_uint8_array(lut)
    uint8_array_to_file(tmp, "lut.txt")
    quit()
    x1 = get_random_x() / pow(2, 2)
    x2 = get_random_x() / pow(2, 2)
    e1 = encode_a_b(x1)
    e2 = encode_a_b(x2)
    d1 = decode_a_b(e1)
    print(f"x1: {x1}")
    print(f"x2: {x2}")
    print(f"e1: {e1}")
    print(f"d1: {d1}")
    # e2 = encode_a_b(x2)
    tmp1 = e1 + e2
    tmp2 = e1 - e2
    tmp3 = pbs(tmp1, lut)
    tmp4 = pbs(tmp2, lut)
    tmp5 = tmp3 - tmp4
    tmp6 = decode_a_b(tmp5)
    ans = x1 * x2

    # print(f"x1: {x1}")
    # print(f"x2: {x2}")
    print()
    print(f"tmp6: {tmp6}")
    print(f"ans: {ans}")
