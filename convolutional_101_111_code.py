from functools import reduce

def Convolutional_101_111_encoder(message: str) -> str:
    if len(message) >= 3:
        b = (int(message[0])+int(message[2]))%2
        c = (int(message[0])+int(message[1])+int(message[2]))%2
        return str(b)+str(c)

def Convolutional_101_111_full_message_encoder(message: str, const=True) -> str:
    if const:  #   старт   -   стоп-ные символы
        message = '00'+message+'00' # для возврата кодера в состояние 00
    out = ''
    for i in range(len(message)):
        code_word = Convolutional_101_111_encoder(message[i:i+3])
        #print(message[i:i+3])
        if code_word is None: break
        out += code_word
    return out


def Convolutional_101_111_full_message_decoder(code: str, p = 1) -> str:
    # пороговый метод, оптимальный порог p = 1
    code = code+'00'
    a = []  # восстанавливаем информационные символы
    # выпишем проверочные символы, в данном случае, будем использовать проверочный символ b ( 1,3,5-ый...)
    b = []  # а массив в python 3 начинается с 0, то есть 0,2,4-й и так далее
    b_ = [] # вычисляем проверочный бит на основе информационных

    for i in range(len(code)//2-1):
        # первый бит отсекаем (вводим задержку), т.к. мы восстанавливали не i-ый, а i-1 информационный символ
        # а соответсвенно первый бит будет являться битом, предшествующим первому закодированному ( исходного сообщ. )
        a += [(int(code[i*2+2])+int(code[i*2+3]))%2]  # восстанавливаем информационные символы
        b += [int(code[i*2])]

    for i in range(len(a)):
        j = i-2
        if j < 0: prev_a = 0
        else: prev_a = a[j]
        b_ += [(prev_a+a[i])%2]  # вычисляем проверочный бит на основе информационных

    # исправление ошибок
    a_ = []
    for i in range(len(a)-2):
        p_ = (b[i]+b_[i])%2+(b[i+2]+b_[i+2])%2
        if p_ > p:
            a_ += [(a[i]+1)%2]
            b_[i+2] = (b_[i+2]+1)%2
        else: a_ += [a[i]]

    return ''.join(map(str,a_))

#code = Convolutional_101_111_full_message_encoder('100001')
#print(code)
#print(Convolutional_101_111_full_message_decoder(code))