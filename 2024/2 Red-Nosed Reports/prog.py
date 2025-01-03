from re import X
import tools
from enum import Enum
from typing import Iterable, Iterator, List, Self, Sequence, Tuple

def parse_line(line: str) -> List[int]:
    return list(map(int, line.split(' ')))

def is_safe(levels : List[int] ) -> bool:
    return is_safe_dir(levels, -1) or is_safe_dir(levels, 1)

def is_safe_dir(levels : List[int], dir : int) -> bool:
    
    # i=0
    # while True:
    #     n0 = levels[i]
    #     for i1 in range(1, 1+max_unsafe):
    #         n = levels[i+i1]
    #         diff = dir * (n0 - n)
    #         if not ( 0 < diff and diff <= 3 ):
    #             if max_unsafe == 0:
    #                 return False
    #             max_unsafe -= 1
    #         else:
    #             prev = n


    #         pass

    def check_safe(n1, n2):
        diff = dir * (n1-n2)
        return ( 0 < diff and diff <= 3 )


    prev = levels[0]
    pos = 1

    for n in levels[pos:] :
        if not check_safe(prev, n):
            return False
        else:
            prev = n

    return True

def is_safe_if_remove_one(levels : List[int]) -> bool:
    for remove in range(len(levels)):
        pre = levels[:remove]
        post = levels[remove+1:]
        if is_safe(pre+post):
            return True
    return False