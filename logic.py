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

class Base:
    def __init__(self, number:str):
        self.n = number
        self.base: int

    def operator(self, n)-> str:
        ''' process the `n` with appropiate built-in function according to the base. '''
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
        ''' seperate int and float parts from a number'''
        # assert isinstance(n, float), 'type error'

        _int, _, _float = str(n).strip('0').partition('.')
        return _int or 0, _float or '0'

    def float_conversion(self, n:FloatPart) -> str:
        raise NotImplemented('function "float_conversion"')

    def do(self, base: int) -> str:
        raise NotImplemented('function "do"')


class FromDec(Base):

    def float_conversion(self, n:FloatPart) -> str:
        if any(int(i)>=self.base for i in n):
            raise ValueError(f'invalid literal... for base {self.base}')
        
        res=''
        while True:
            if len(res)>=(max_round+1):
                return res+'...'

            int_part, n = self.positional_mul(n)
            res += self.operator(int_part)
            if int(n)==0:
                break

        return res

    def do(self, base: int) -> str:
        self.base = base

        if '.' not in self.n:# non-floating point
            return self.operator(self.n)
        
        _int, _float = self.fmod(self.n)
        return f'{self.operator(_int)}.{self.float_conversion(_float)}'

    def __repr__(self) -> str:
        return str({
            "bin": self.bin,
            "oct": self.oct,
            "hex": self.hex
        })


class ToDec(Base):
    def float_conversion(self, n:FloatPart) -> str:
        res=0
        for local_value, num in enumerate(n):
            local_value+=1
            num=int(num, self.base)# base is required for hex

            if num>=self.base:
                raise ValueError(f'invalid literal ... for base {self.base}')

            res+=num/pow(self.base, local_value)

        return self.fmod(res)[-1]

    def do(self, base: int) -> str:
        self.base = base

        if self.base==10: return self.n
        if '.' not in self.n:# non-floating point
            return str(int(self.n, base=base))
        
        _int, _float = self.fmod(self.n)
        return f'{int(_int, base)}.{self.float_conversion(_float)}'


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
                print('[#]', ToDec(inp).do(16))

        except KeyboardInterrupt:
            break
        except:
            print('[-] Error.')

