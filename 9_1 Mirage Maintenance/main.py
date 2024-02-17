import os
import prog
from pathlib import Path
import time


t0 = time.perf_counter()

input = os.path.join(os.path.dirname(__file__), 'input.txt')
lines = Path(input).read_text().splitlines()

sum = 0

t1 = time.perf_counter()


for l in lines:
    ints = list(map(lambda s: int(s), l.split(' ')))
    p = prog.Predictor(ints)
    sum += p.next_el

t2 = time.perf_counter()
print(f'sum:{sum}  dt1:{t1-t0}  dt2:{(t2-t1)}') # 1743490457


