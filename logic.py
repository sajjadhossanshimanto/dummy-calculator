import sys
import os
from typing import TypeVar, Tuple


base = 2
max_round = 10

ope = {
    2: bin,
    8: oct,
    16: hex
}
if base not in ope:
    print('[-] wrong base provided.')
    sys.exit()

FloatPart = TypeVar('FloatPart')# str
IntPart = TypeVar('IntPart', int, str)


class Converter:
    base=2

    def __new__(cls, number):
        return

    def operator(self, n)-> str:
        return ope[base](int(n))[2:]

    def positional_mul(self, number:FloatPart)-> Tuple[IntPart, FloatPart]:
        # assert isinstance(number, str)

        pre_len = len(number)
        number = str(int(number)*base)
        number.rstrip('0')
        cur_len = len(number)

        start = cur_len-pre_len
        return number[:start] or 0, number[start:] or '0'

    def fmod(self, n:str) -> Tuple[IntPart, FloatPart]:
        # assert isinstance(n, float), 'type error'

        _int, _, _float = str(n).strip('0').partition('.')
        return _int or 0, _float or '0'

    def float_to_bin(self, n:FloatPart) -> str:
        res='.'
        while True:
            if len(res)>=(max_round+1):
                return res+'...'

            int_part, n = self.positional_mul(n)
            res += self.operator(int_part)
            if int(n)==0:
                break

        return res

    def dec_to_bin(self, n:str) -> str:
        if '.' not in n:# non-floating point
            return self.operator(n)
        
        _int, _float = self.fmod(n)
        return self.operator(_int) + self.float_to_bin(_float)          


if __name__=='__main__':
    def clear():
        os.system('clear')

    clear()
    while True:
        try:
            inp = input('>>> ')
            if inp=='e': break
            elif inp=='c': clear()
            else:
                float(inp)# check for invalid arguments
                print('[#]', dec_to_bin(inp))
                
        except KeyboardInterrupt:
            break
        except:
            print('[-] invalid entry.')

