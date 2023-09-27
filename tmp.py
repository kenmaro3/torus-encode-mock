import numpy as np


def int32_to_uint8_array(x):
    res = []
    for i in range(4):
        tmp = x >> ((4-i-1) * 8)
        print(tmp)
        res.append(tmp & ((1 << 8) - 1))
    return res


def uint8_array_to_int32(x):
    res = x[3]
    for i in range(1, 4):
        res += x[3-i] << (i * 8)
    return res


if __name__ == "__main__":
    x = 1000
    tmp = int32_to_uint8_array(x)
    print(tmp)
    tmp2 = uint8_array_to_int32(tmp)
    print(tmp2)
