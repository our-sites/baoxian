# coding:utf-8
# write  by  zhou
# int 和sting 互相转换的工具
import string


def _decimalToAny(num, n):
    "n 可以小于等于 62"
    _ = string.ascii_letters
    baseStr = dict(zip(range(10, 10 + len(_) + 1), _))
    new_num_str = ""
    while num != 0:
        remainder = num % n
        if n > remainder > 9:
            remainder_string = baseStr[remainder]
        else:
            remainder_string = str(remainder)
        new_num_str = remainder_string + new_num_str
        num = num / n
    return new_num_str


def _anyToDecimal(num, n):
    "n 可以小于等于 62"
    _ = string.ascii_letters
    baseStr = dict(zip(_,range(10, 10 + len(_) + 1)),**dict([(str(i),i)for i in range(0,10)]))
    new_num = 0
    nNum = len(num) - 1
    for i in num:
        new_num = new_num + baseStr[i] * pow(n, nNum)
        nNum = nNum - 1
    return new_num


def int2string(int):
    return  _decimalToAny(int,61)

def string2int(str):
    return _anyToDecimal(str,61)

if __name__=="__main__":
    a=122345001234
    b= int2string(a)
    print b
    c= string2int(b)
    print c
