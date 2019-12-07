# -*- coding: utf-8 -*-
import numpy as np
from itertools import permutations
import unittest

from day_5 import Computer

class Test(unittest.TestCase):
    
    def test_1(self):
        phases = (4,3,2,1,0)
        code = np.array([3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0])
        self.assertEqual(run(phases, code), 43210)
        
    def test_2(self):
        phases = range(5)
        opcode = np.array([3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0])
        self.assertEqual(run(phases, opcode), 54321)

    def test_3(self):
        phases = (1,0,4,3,2)
        opcode = np.array([3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0])
        self.assertEqual(run(phases, opcode), 65210)
        
    def test_5(self):
        phases = (9,8,7,6,5)
        code = np.array([3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5])
        self.assertEqual(run_loop(phases, code), 139629729)
        
    def test_6(self):
        phases = (9,7,8,5,6)
        code = np.array([3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10])
        self.assertEqual(run_loop(phases, code), 18216)


def run(phases, code: np.array, val=0):
    for phase in phases:
        amp = Computer(code, phase)
        val = amp.execute(val)
        #print(f'{phase=}, {val=}')
    return val


def run_loop(phases, code: np.array):
    """
    Provide each amplifier its phase setting at its first input instruction; all further input/output instructions are for signals.
    -> only set phase during amp.__init__()
    
    Don't restart the Amplifier Controller Software on any amplifier during this process. 
    -> keep the internal state of the array
    
    Each one should continue receiving and sending signals until it halts.
    -> the next amplifier starts when previous one waits for new input and has produced output
    -> amp halts when state 99 reached
    """
    val = 0
    amps = [Computer(code, p) for p in phases]
    while not amps[-1].done:
        for j in range(len(amps)):
            val = amps[j].execute(val)
            # print(f'{j=}:', amps[j])
    return val
        

if __name__ == '__main__':
    unittest.main()
    d = np.fromstring(open('day_7_input.csv').read(), sep=',', dtype=np.int32)
    best = max(run(p,d) for p in permutations(range(5)))
    print('1)', best)
    
    # integers from 5 to 9, again each used exactly once
    best_2 = max(run_loop(p,d) for p in permutations(range(5,10)))
    print('2)', best_2)
    

        
