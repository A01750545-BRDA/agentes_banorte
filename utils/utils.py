import inspect
import os

def open_obj(object):
    os.system(f'open {inspect.getsourcefile(object)}')

def print_heading(heading: str, 
                  separator: str = '=', 
                  total_len: int = 100):
    
    k = (total_len - len(heading) + 2)//2
    print(k * separator, f' {heading} ', k * separator)