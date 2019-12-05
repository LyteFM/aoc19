# -*- coding: utf-8 -*-
import numpy as np
import unittest

class TestOpcode(unittest.TestCase):
    
    def test_1(self):
        data = np.array(['1','9','10','3','2','3','11','0','99','30','40','50'], dtype=np.int32)
        self.assertEqual(run_opcode(data), 3500)


def run_opcode(d: np.array):
    """
    opcode - either 1, 2, or 99
    99 means that the program is finished and should immediately halt.
    unknown opcode means something went wrong.
    opcode 1 - adds numbers
    opcode 2 - multiplies
    when done with one - move to next, skipping four
    """
    i = 0
    while i < len(d):
        if d[i] == 99:
            # print('completed at i = ', i)
            break
        elif d[i] == 1:
            d[d[i+3]] = d[d[i+2]] + d[d[i+1]]
            i += 4
        elif d[i] == 2:
            d[d[i+3]] = d[d[i+2]] * d[d[i+1]]
            i += 4
        else:
            print('error at i = ', i)
            break
    return d[0]


# 2)
# pos 1, pos2: vals between 0 and 99
# 19690720 as output wanted
# 688 ms ± 14.9 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
def find_start(target: int, d: np.array):
    for noun in range(100):
        for verb in range(100):
            opcode = d.copy()
            opcode[1] = noun
            opcode[2] = verb
            res = run_opcode(opcode)
            if res == 19690720:
                return noun, verb
    return None

# 1.01 s ± 14.1 ms per loop (mean ± std. dev. of 7 runs, 1 loop each)
# computes _all_ 10000 values, not stopping at 6577 -> running opcode takes same time.
def find_start_array(target: int, d: np.array):
    mat = np.repeat(d.reshape(-1,1), 10000, axis=1)
    mat[1] = np.repeat(np.arange(100), 100)
    mat[2] = np.tile(np.arange(100), 100)
    vals = np.apply_along_axis(run_opcode, 0, mat)
    idx = np.where(vals==19690720)[0][0]
    # already fulfills 100*n + v :)
    return idx


if __name__ == '__main__':
    
    unittest.main()
    
    d = np.loadtxt('day_2_input.csv', dtype=np.int32)

    # 1)
    first = d.copy()
    first[1] = 12
    first[2] = 2
    print('1) answer: ', run_opcode(first))
    
    # 2)
    n, v = find_start(19690720, d)
    print('2) answer:', 100*n + v)
    print('2) with arrays:', find_start_array(19690720, d))