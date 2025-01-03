from typing import List
import unittest
import prog
import tools

import prog 

pattern1 = \
'''7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9'''.splitlines()


    
class Tests(unittest.TestCase):
    def general(self, expected_results : List[bool], is_safe_method):

        levels_list = list(map(prog.parse_line, pattern1))

        for n, levels, expected in zip(tools.natural_numbers(), levels_list, expected_results):
            actual = is_safe_method(levels)
            errmsg = f'test {n}'
            self.assertEqual(expected, actual, errmsg)

        pass
       
    def test_dot1(self):
        expected_results = [True, False, False, False, False, True]
        self.general(expected_results, prog.is_safe)

    def test_dot2(self):
        expected_results = [True, False, False, True, True, True]
        self.general(expected_results, prog.is_safe_if_remove_one)
        
        actual0 = prog.is_safe([1,3,2,4,5])
        actual1 = prog.is_safe_if_remove_one([1,3,2,4,5])
        actual2 = prog.is_safe([1,2,4,5])
        actual3 = prog.is_safe([1,3,4,5])
        self.assertEqual(False, actual0)
        self.assertEqual(True, actual1)
        self.assertEqual(True, actual2)
        self.assertEqual(True, actual3)

   

if __name__ == '__main__':
    unittest.main()
    
