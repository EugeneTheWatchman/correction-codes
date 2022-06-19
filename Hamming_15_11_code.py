import numpy as np
from functools import reduce

def ChangeMyBase(number, newbase):
    newNum = []
    while number > 0:
        newNum = [number % newbase] + newNum
        number //= newbase
    return newNum

def Stroka(length,base,i = 1):
    while i < base**length:
        stroka = ChangeMyBase(i,base)
        while len(stroka) < length:
            stroka = [0] + stroka
        return stroka,i
    return False


# задание матриц для кода (15,11)
H_15_11 = np.array([[1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0],
                    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 1, 0, 0],
                    [0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 0, 1, 0],
                    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1],]).T
G_15_11 = np.eye(11, 15)
G_15_11[:, 11:15] = H_15_11[0:11]

if False:
    message = [0]*11
    d_15_11 = {}
    for j in range(1):
        result = Stroka(len(message),2,j)  # перебираем все комбинации сообщений из 5-ти сиволов
        if not result: break
        message = result[0]
        code = np.dot(message, G_15_11) % 2
        code = [int(i) for i in code]
        for i in range(len(code)):
            code_ = np.array(code)
            code_[i] = (code_[i]+1)%2
            syndrom = ''.join([str(int(i)) for i in (code_.dot(H_15_11) % 2)])
            #print('syndrom -',syndrom,';','i -',i,';','code -',code_)
            d_15_11[syndrom] = i
        print(d_15_11,'-',message)
else:
    d_15_11 = {'1100': 0, '1010': 1, '0110': 2, '1110': 3, '1001': 4,
               '0101': 5, '1101': 6, '0011': 7, '1011': 8, '0111': 9,
               '1111': 10, '1000': 11, '0100': 12, '0010': 13, '0001': 14}

def Hamming_15_11_encoder(mes: str) -> str:
    message = [int(i) for i in mes]+[0]*(11-len(mes))

    code = [int(i) for i in (np.dot(message, G_15_11) % 2)]
    #print(code)
    for i in range(11,1,-1):
        if len(mes) < i:
            code.pop(i-1)
    return reduce(lambda x, y: str(x) + str(y), code)

def Hamming_15_11_decoder(code_: str) -> str:
    code = [int(i) for i in code_]
    for i in range(5,16):  # i = 5,6,...,14,15
        if len(code_) < i:
            #print(code)
            code.insert(i-5,0)
            #print(code)
    syndrom = np.dot(code, H_15_11) % 2
    syndrom = ''.join([str(int(i)) for i in syndrom])
    #print(syndrom)
    if syndrom == '0000':  # нет ошибок
        return code_[0:len(code_) - 4]
    item = d_15_11[syndrom]
    if item > len(code_): # если исправлять бит нужно, которого нет ( для усеченных кодов )
        return code_[0:len(code_) - 4]  # то передаем только информационные биты, без исправления
    code[item] = (code[item] + 1) % 2  # исправляем ошибочный бит
    return reduce(lambda x, y: str(x) + str(y), code)[0:len(code_) - 4]


'''
message = '1000'
code = Hamming_15_11_encoder(message)
print(code, '-',code := '10101100')

decode = Hamming_15_11_decoder(code)
print(message,'=' if message == decode else '!=', decode)
print(len(message),'-',len(decode))'''