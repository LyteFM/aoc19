# -*- coding: utf-8 -*-
import numpy as np

# take its mass, divide by three, round down, and subtract 2.
d = np.loadtxt('day_1_input.csv', dtype=np.int32)
fuel = d//3-2
print('1)', fuel.sum())

# recursively add fuel for fuel
def get_add(x):
    ret = x//3-2
    return 0 if ret <= 0 else ret + get_add(ret)

fuel += np.vectorize(get_add)(fuel)
print('2)', fuel.sum())