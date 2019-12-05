# -*- coding: utf-8 -*-
import unittest

MIN_VALUE=245182
MAX_VALUE=790572

class Test(unittest.TestCase):
    
    def test_part1(self):
        self.assertTrue(is_possible_password(122345))
        self.assertFalse(is_possible_password(223450))
        self.assertTrue(is_possible_password(111111))
        self.assertFalse(is_possible_password(123789))
        
    def test_part2(self):
        self.assertTrue(is_possible_password(112233, True))
        self.assertTrue(is_possible_password(111122,True))
        self.assertFalse(is_possible_password(123444, True))
        self.assertTrue(is_possible_password(338888, True))
        

def is_possible_password(number, only_two_consecutive=False):
    """
    It is a six-digit number. (not tested here)
    The value is within the range given in your puzzle input.
    Two adjacent digits are the same (like 22 in 122345).
    Going from left to right, the digits never decrease; they only ever increase or stay the same (like 111123 or 135679).
    Part 2: the two adjacent matching digits may not part of a larger group of matching digits. (but other are ok...)
    """
    prev = 0
    has_double = False
    consecutive_count=0
    has_sequence_of_two=False
    for power in range(5, -1, -1):
        digit = number // 10**power # who needs strings or sorted() x) 
        
        if digit == prev:
            has_double = True
            consecutive_count+=1
            if power==0 and consecutive_count==1:
                has_sequence_of_two=True
        else:
            if digit < prev:
                return False
            if consecutive_count==1:
                has_sequence_of_two=True
            consecutive_count=0

        prev = digit
        number -= digit*10**power
    
    return has_double and (has_sequence_of_two or not only_two_consecutive)


if __name__ == '__main__':
    unittest.main()
    first_pws = set()
    second_pws = set()
    for b in (False, True):
        pw_count=0
        for pw in range(MIN_VALUE, MAX_VALUE+1):
            if is_possible_password(pw, b):
                pw_count+=1
                if b:
                    second_pws.add(pw)
                else:
                    first_pws.add(pw)
        print(pw_count) # 575 too low for part 2 -> accidentally excluded if _any_ sequence > 2
