import os
from pathlib import Path
import prog 
import tools
from hashmap import HashMap

# entry point
def main():

    input_txt = os.path.join(os.path.dirname(__file__), 'input.txt')
    input_str = Path(input_txt).read_text()

    sum1 = prog.sum_hash_line(input_str)

    operations = prog.split_input(input_str)
    hmap = HashMap()
    for op in operations:
        hmap.perform_operation(op)
            
    sum2 = hmap.calc_focal_length_total()

    print(f'sum1:{sum1}  sum2:{sum2} ')  # sum1:517965  sum2:xxx
    
    # after 141 spin cycles (cycle detected, at 107 len=34)
    # force_2:90551 after 160 spin cycles (cnt=126, diff=34)
    # force_1:110677  force_2:90551

if __name__ == '__main__':
    main() 