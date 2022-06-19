from functools import reduce
s = 2

def Convolutional_111_101_encoder(message: str) -> str:
    if len(message) >= 3:
        a = (int(message[0])+int(message[1])+int(message[2]))%2
        b = (int(message[0])+int(message[2]))%2
        return str(a)+str(b)

def Convolutional_101_111_full_message_encoder(message: str, const=True) -> str:
    if const:  #   старт   -   стоп-ные символы
        message ='0'*(s//2)+'00'+message+'00'+'0'*(s//2+s%2)
    out = ''
    for i in range(len(message)):
        code_word = Convolutional_111_101_encoder(message[i:i+3])
        if code_word is None: break
        out += code_word
    return out

if True:

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
    d = dict()  # создаем список соответствий: код - кодируемое сообщение
    for i in range(10000):
        result = Stroka(5+s,2,i)  # перебираем все комбинации сообщений из 5-ти сиволов
        if not result: break
        message = reduce(lambda x, y: str(x) + str(y), result[0])  # преобразование в строку
        code = Convolutional_101_111_full_message_encoder(message, False)
        d[code] = message  # добавляем новую строку с соответствием

def Convolutional_111_101_decoder(code: str) -> str:
    if len(code) >= 6+s*2:
        min_Hamming_distanse = len(code)+1  # len(code) + 1
        for possible_code in d.keys():
            Hamming_distanse = 0
            for i,j in zip(code, possible_code):
                if i != j:  # если не равны соответствующие символы, то прибавляем 1 к расстоянию Хэмминга
                    Hamming_distanse += 1
                    if Hamming_distanse >= min_Hamming_distanse:  # если расстояние Хэмминга больше минимального,
                        break                               # нам не подходит этот возможный вариант передаваемого кода
            else:  # срабатывает только тогда, когда break не был вызван
                min_Hamming_distanse = Hamming_distanse
                transmitted_code = possible_code  # тут в конце концов останется тот код, чье расстояние Хэмминга до принятого минимально
        return d[transmitted_code][2+s//2]  # центральный символ

def Convolutional_101_111_full_message_decoder(code: str) -> str:
    out = ''
    for i in range(len(code)):
        message = Convolutional_111_101_decoder(code[i*2:i*2+6+s*2])
        if message == None: break
        else: out += message
    return out
