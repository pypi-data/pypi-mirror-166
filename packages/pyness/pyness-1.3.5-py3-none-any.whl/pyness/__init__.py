import random
import subprocess
import os
import time
class cheats():
    start = time.time()
    def runtime():
        return int(time.time() - cheats.start)
    def clear():
        # next update linux will be added but for now it's for window
        os.system("cls")
    def getfileformat(file):
        size = len(file)
        output = []
        check = 0
        file = file[::-1]
        for i in range(0,size):
            work = file[check]
            output.append(work)
            if work == '.':
                output= convert.list_to_str(output)
                output = output[::-1]
                return output
            check += 1
class convert():
    def str_to_list(string):
        list1=[]
        list1[:0]=string
        return list1

    def list_to_str(list):
        key=''.join([str(x) for x in list])
        return key

    # def photo(filename,format):
    #     file = cheats.getfileformat(filename)
    #     img = Image.open(filename)
    #     img = img.convert('RGB')
    #     img.save(f'{filename}{format}')
    #     print(f"{file} is been converted to {format}")

def update():
    subprocess.call("pip install pyness -U",shell=True)

def bar(total,amount,length,background='-',border='||',looks='█'):
    if amount > total:
        amount = total
    output = int(amount*100/total)
    progress = int(amount*length/total)
    background = background*(length-progress)
    looks = f'{looks}'*progress
    if output == 100:
        final = f"{border[0]}{looks + background}{border[1]} Complete"
    else:
        final = f"{border[0]}{looks + background}{border[1]} {output}%"
    return final

def fps():
    start_time = time.time()
    time.sleep(0.0001)
    fps = f"{1.0 / (time.time() - start_time)}"[:2]
    return fps

def key(size,number=True,upper=True,symbol=True,lower=True):
    lower_ = 0
    upper_ = 0
    number_ = 0
    symbol_ = 0
    _lower_ = ''
    _upper_ = ''
    _number_ = ''
    _symbol_ = ''
    if number == True:
        number = '1234567890'
    if upper == True:
        upper = 'QWERTYUIOPASDFGHJKLZXCVBNM'
    if symbol == True:
        symbol = '@#$%&!'
    if lower == True:
        lower = 'qwertyuiopasdfghjklzxcvbnm'
    if number == 1:
        raise ValueError("number (1 == True) so pls use something higher than 1")
    if upper == 1:
        raise ValueError("upper (1 == True) so pls use something higher than 1")
    if lower == 1:
        raise ValueError("lower (1 == True) so pls use something higher than 1")
    if symbol == 1:
        raise ValueError("symbol (1 == True) so pls use something higher than 1")
    if type(number) == str:
        number = number
    if type(upper) == str:
        upper = upper
    if type(symbol) == str:
        symbol = symbol
    if type(lower) == str:
        lower = lower
    if number == False:
        number = ""
    if upper == False:
        upper = ""
    if symbol == False:
        symbol = ""
    if lower == False:
        lower = ""
    if type(number) == int:
        number_ = number
        _number_ = random.choices('1234567890', k = number)
        number = ''
    if type(upper) == int:
        upper_ = upper
        _upper_ = random.choices('QWERTYUIOPASDFGHJKLZXCVBNM', k = upper)
        upper = ''
    if type(symbol) == int:
        symbol_ = symbol
        _symbol_ = random.choices('@#$%&!', k = symbol)
        symbol = ''
    if type(lower) == int:
        lower_ = lower
        _lower_ = random.choices('qwertyuiopasdfghjklzxcvbnm', k = lower)
        lower = ''
    if size < lower_ + upper_ + number_ + symbol_:
        raise Exception("Can't the size is higher than it requirement")

    _number_ = convert.str_to_list(_number_)
    _upper_ = convert.str_to_list(_upper_)
    _lower_ = convert.str_to_list(_lower_)
    _symbol_ = convert.str_to_list(_symbol_)
    number = convert.str_to_list(number)
    upper = convert.str_to_list(upper)
    lower = convert.str_to_list(lower)
    symbol = convert.str_to_list(symbol)

    key = []
    all_ = _number_ + _upper_ + _lower_ + _symbol_
    all = number + upper + lower + symbol
    try:
        for i in range(0,size-(lower_ + upper_ + number_ + symbol_)):
            random.shuffle(all)
            shuff = [random.choice(all)]
            c = random.choice(shuff)
            key.append(c)
    except IndexError:
        key = []
    key = key
    all = all_ + key
    random.shuffle(all)
    return convert.list_to_str(all)
#-------------------------------------------------------------------------------------------------------------------