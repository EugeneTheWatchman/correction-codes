
def Convolutional_Fink_encoder(message: str, s: int) -> str:
    i = s
    # s - шаг, но массив начинается с нуля и i-s не может быть меньше нуля
    if len(message) > (i+s+1):
        # сложение по модулю 2 двух информационных символов 0 и 2s+1
        b = (int(message[i-s])+int(message[i+s+1]))%2
        return message[i]+str(b)


def Convolutional_Fink_full_message_encoder(message: str, s=0, const=True) -> str:
    if const: 
        message = '0'*(s*3+1) + message + '0'*((s+1)*2+s)
        #message += '0'*s*2
    out = ''
    for i in range(len(message)):
        code_word = Convolutional_Fink_encoder(message[i:i + 2 + s * 2], s)
        if code_word == None: break
        out += code_word
    return out
