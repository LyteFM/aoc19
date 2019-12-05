# -*- coding: utf-8 -*-
import numpy as np
import unittest

class TestOpcode(unittest.TestCase):
    
    def test_comparisons(self):
        first_arr = np.array([3,9,8,9,10,9,4,9,99,-1,8])
        self.assertEqual(run_opcode(first_arr, in_number=8), 1)
        self.assertEqual(run_opcode(first_arr), 0)
        
        second_arr = np.array([3,9,7,9,10,9,4,9,99,-1,8])
        self.assertEqual(run_opcode(second_arr, in_number=8), 0)
        self.assertEqual(run_opcode(second_arr), 1)
        
        third_arr = np.array([3,3,1108,-1,8,3,4,3,99])
        self.assertEqual(run_opcode(third_arr, in_number=8), 1)
        self.assertEqual(run_opcode(third_arr), 0)
        
        fourth_arr = np.array([3,3,1107,-1,8,3,4,3,99])
        self.assertEqual(run_opcode(fourth_arr), 1)
        self.assertEqual(run_opcode(fourth_arr, in_number=8), 0)
        
    def test_jumps(self):
        jump_1 = np.array([3,12,6,12,15,1,13,14,13,4,13,99,-1,0,1,9])
        jump_2 = np.array([3,3,1105,-1,9,1101,0,0,12,4,12,99,1])
        
        self.assertEqual(run_opcode(jump_1), 1)
        self.assertEqual(run_opcode(jump_1, in_number=0), 0)
        self.assertEqual(run_opcode(jump_2), 1)
        self.assertEqual(run_opcode(jump_2, in_number=0), 0)
        
    def test_larger(self):
        jumps = np.array([3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
                          1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
                          999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99])
        self.assertEqual(run_opcode(jumps), 999)
        self.assertEqual(run_opcode(jumps, in_number=8), 1000)
        self.assertEqual(run_opcode(jumps, in_number=20), 1001)
    
    
def get(d: np.array, pos: int, immediate: bool):
    return d[pos] if immediate else d[d[pos]]


def run_opcode(in_arr: np.array, in_number=1):
    d = in_arr.copy()
    i = 0
    while True:
        full_op = str(d[i]).zfill(5)
        # parameter mode 0, position mode -> param is value stored at that address
        # parameter mode 1, intermediate mode -> is simply the passed value
        # Parameter modes are single digits, one per parameter, read right-to-left from the opcode: the first parameter's 
        # mode is in the hundreds digit, the second parameter's mode is in the thousands digit, the third parameter's mode 
        # is in the ten-thousands digit, and so on. Any missing modes are 0.
        first_immediate = full_op[2] == '1'
        second_immediate = full_op[1] == '1'
        assert full_op[0] == '0'
        # The opcode is a two-digit number based only on the ones and tens digit of the value, 
        # that is, the opcode is the rightmost two digits of the first value in an instruction
        instruction = int(full_op[3:])
        if instruction == 99:
            # print('completed at i = ', i)
            break
        
        first = get(d, i+1, first_immediate)
        if instruction in (1,2):
            second = get(d,i+2, second_immediate)
            d[d[i+3]] = first + second if instruction == 1 else first * second
            i += 4
        elif instruction == 3:
            # Opcode 3 takes a single integer as input and saves it to the position given by its only parameter. 
            # For example, the instruction 3,50 would take an input value and store it at address 50.
            d[d[i+1]] = in_number
            i += 2
        elif instruction == 4:
            # Opcode 4 outputs the value of its only parameter. 
            # For example, the instruction 4,50 would output the value at address 50.
            output = first
            # print(f'Output: {output}')
            i += 2
        # Opcode 5 / 6 adjust the instruction pointer if first parameter is not / is 0, else just continue.
        elif instruction in (5,6):
            if instruction == 5 and first != 0 or instruction == 6 and first == 0:
                i = get(d,i+2, second_immediate)
            else:
                i += 3
        # Opcode 7 / 8 is less than/equals: if the first parameter is less than/equal to the second parameter, 
        # it stores 1 in the position given by the third parameter. Otherwise, it stores 0.
        elif instruction == 7:
            d[d[i+3]] = 1 if first < get(d,i+2, second_immediate) else 0
            i += 4
        elif instruction == 8: 
            d[d[i+3]] = 1 if first == get(d,i+2, second_immediate) else 0
            i += 4
        else:
            print('ERROR at i = ', i, ', value: ', d[i], 'instruction:', instruction)
            break
    return output

if __name__ == '__main__':
    unittest.main()
    
    d = np.loadtxt('day_5_input.csv', delimiter=',', dtype=np.int32)
    print('Part 1:', run_opcode(d))
    print('Part 2:', run_opcode(d, 5))




