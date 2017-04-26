#!/usr/bin/env python
#*_* coding: utf-8 *_*
import re

def handle_special_occactions(plus_and_minus_operators,multiply_and_dividend):
    '''有时会出现这种情况 , ['-', '-'] ['1 ', ' 2 * ', '14969036.7968254'],2*...后面这段实际是 2*-14969036.7968254,需要特别处理下,太恶心了'''
    for index,i in enumerate(multiply_and_dividend):
        i = i.strip()
        if i.endswith("*") or i.endswith("/"):
            multiply_and_dividend[index] = multiply_and_dividend[index] + plus_and_minus_operators[index] + multiply_and_dividend[index+1]
            del multiply_and_dividend[index+1]
            del plus_and_minus_operators[index]
    return  plus_and_minus_operators,multiply_and_dividend

def remove_duplicates(str):
    str = str.replace("++","+")
    str = str.replace("+-","-")
    str = str.replace("-+","-")
    str = str.replace("--","+")
    str = str.replace("- -","+")
    return str
def multiAndDivi(str):
    operate = re.findall("[*/]", str)
    operate_argv = re.split("[*/]", str)
    res = None

    for index, i in enumerate(operate_argv):
        if res:
            if operate[index - 1] == '*':
                res *= float(i)
            else:
                res /= float(i)
        else:
            res = float(i)
    return res

def compute(str):
    str = str.strip('()')
    str = remove_duplicates(str)
    operate = re.findall("[+-]", str)
    operate_argv = re.split("[+-]", str)
    if len(operate_argv[0].strip()) == 0:
        operate_argv[1] = operate[0] + operate_argv[1]
        del operate[0]
        del operate_argv[0]
    print(operate,operate_argv)
    operate, operate_argv = handle_special_occactions(operate, operate_argv)
    for index, i in enumerate(operate_argv):

        if re.search("[*/]", i):
            res = multiAndDivi(i)
            operate_argv[index] = res

    print(operate, operate_argv)

    res_total = None
    for index,i in enumerate(operate_argv):
        if res_total:
            if operate[index-1] == '+':
                res_total += float(i)
            else:
                res_total -= float(i)
        else:
            res_total = float(i)

    return res_total

def calc(str):
    flag = True
    while flag:
        m = re.search("\([^()]*\)", str)
        if m:
            result = compute(m.group())
            result = "%f" % result
            str = str.replace(m.group(), result)
            print(str)
        else:
            result = compute(str)
            flag = False
            return result



# def calc(str):
#     m = re.search("\([^()]*\)", str)
#     result = compute(m.group())
#     result = "%f" % result
#     str = str.replace(m.group(), result)
#     print(str)
#     #result = compute(str)
#     print("--------------")

#calc("1 - 2 * ( (60-30 +(-9-2-5-2*3-5/3-40*4/2-3/5+6*3) * (-9-2-5-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )")
#calc("1 - 2 * ( (60-30 +-86.266667 * (-9-2-5-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )")
#calc("1 - 2 * ( (60-30 +-86.266667 * 173520.880952) - (-4*3)/ (16-3*2) )")
#calc("1 - 2 * ( -14969038.054633 - (-4*3)/ (16-3*2) )")
#calc("1 - 2 * ( -14969038.054633 - -12.000000/ (16-3*2) )")
#calc("1 - 2 * ( -14969038.054633 - -12.000000/ 10.000000 )")
#calc("1 - 2 * -14969036.854633")

if __name__ == '__main__':
    result = calc("1 - 2 * ( (60-30 +(-9-2-5-2*3-5/3-40*4/2-3/5+6*3) * (-9-2-5-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )")
    print('计算结果为：{0}'.format(result))

