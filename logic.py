import os
from typing import TypeVar, Tuple


max_round = 10
ope = {
    2: bin,
    8: oct,
    16: hex
}

FloatPart = TypeVar('FloatPart')# str
IntPart = TypeVar('IntPart', int, str)


class Convert:
    def __init__(self, number:str):
        self.n = number

        # for self.base, v in ope.items():
        #     setattr(self, v.__name__, self.do())

    def operator(self, n)-> str:
        return ope[self.base](int(n))[2:]

    def positional_mul(self, number:FloatPart)-> Tuple[IntPart, FloatPart]:
        # assert isinstance(number, str)

        pre_len = len(number)
        number = str(int(number)*self.base)
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

    def do(self, base) -> str:
        self.base = base 

        if '.' not in self.n:# non-floating point
            return self.operator(self.n)
        
        _int, _float = self.fmod(self.n)
        return self.operator(_int) + self.float_to_bin(_float)          

    def __repr__(self) -> str:
        return str({
            "bin": self.bin,
            "oct": self.oct,
            "hex": self.hex
        })


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
                print('[#]', Convert(inp).do(2))

        except KeyboardInterrupt:
            break
        except:
            print('[-] Error.')

