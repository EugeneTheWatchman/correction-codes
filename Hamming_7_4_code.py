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

# задание порождающей и проверочной матриц для кода (7,4)
# именное такое, чтобы усеченные коды были с такими же синдромами
G_7_4 = np.array([[1, 0, 0, 0, 1, 1, 1],
                  [0, 1, 0, 0, 1, 1, 0],
                  [0, 0, 1, 0, 1, 0, 1],
                  [0, 0, 0, 1, 0, 1, 1], ])
H_7_4 = np.empty([7, 3])
H_7_4[4:7] = np.eye(3, 3)
H_7_4[0:4] = G_7_4[:, 4:7]


if False:
    message = [0,0,0,0]
    d_7_4 = {}
    for j in range(1000):
        result = Stroka(len(message),2,j)  # перебираем все комбинации сообщений из 5-ти сиволов
        if not result: break
        message = result[0]
        code = np.dot(message, G_7_4) % 2
        code = [int(i) for i in code]
        for i in range(len(code)):
            code_ = np.array(code)
            code_[i] = (code_[i]+1)%2
            syndrom = ''.join([str(int(i)) for i in (code_.dot(H_7_4) % 2)])
            #print('syndrom -',syndrom,';','i -',i,';','code -',code_)
            d_7_4[syndrom] = i
        print(d_7_4,'-',message)
        # print('\t'.join(map(lambda x: str(x),code)))#,'-',message)
else: d_7_4 = {'111': 0, '110': 1, '101': 2, '011': 3, '100': 4, '010': 5, '001': 6}

def Hamming_7_4_encoder(mes: str) -> str:
    message = [int(i) for i in mes]+[0]*(4-len(mes))

    code = [int(i) for i in (np.dot(message, G_7_4) % 2)]
    if len(mes) < 4:  # 012_
        code.pop(3)  # 012_456
    if len(mes) < 3:  # 01__
        code.pop(2)  # 01__345
    if len(mes) < 2:  # 0___
        code.pop(1)  # 0___234
    return reduce(lambda x, y: str(x) + str(y), code)

def Hamming_7_4_decoder(code_: str) -> str:
    code = [int(i) for i in code_]
    if len(code_) < 5:  # 0___
        code.insert(1,0)  # 0|__234
    if len(code_) < 6:
        code.insert(2,0)
    if len(code_) < 7:
        code.insert(3,0)
    syndrom = np.dot(code, H_7_4) % 2
    syndrom = ''.join([str(int(i)) for i in syndrom])
    if syndrom == '000':  # нет ошибок
        return code_[0:len(code_) - 3]
    item = d_7_4[syndrom]
    print(item)
    if item > len(code_)-1: # если исправлять бит нужно, которого нет ( для усеченных кодов )
        return code_[0:len(code_) - 3]  # то передаем только информационные биты, без исправления
    code[item] = (code[item] + 1) % 2  # исправляем ошибочный бит
    return reduce(lambda x, y: str(x) + str(y), code)[0:len(code_) - 3]

'''
message = '1001'
code = Hamming_7_4_encoder(message)
print(code, '-', code := code)
decode = Hamming_7_4_decoder(code)
print(message, '-', decode)
'''
