
def Convolutional_Fink_decoder(code: str, s: int) -> int:
    i = 2*s+2
    if len(code) > (4*s+2)*2:
        a1 = int(code[0])
        a2 = int(code[(2*s+1)*2])
        a3 = int(code[(4*s+2)*2])
        # print(f'a1 = {a1}, a2 = {a2}, a3 = {a3}')
        # print(f'a1 + a2 = {a1+a2} =? b1 = {code[i-1]}, {(a1+a2)%2 == int(code[i-1])}')
        # print(f'a2 + a3 = {a2+a3} =? b2 = {code[i+1]}, {(a2+a3)%2 == int(code[i+1])}')
        if (a1+a2)%2 != int(code[i-1]) and (a2+a3)%2 != int(code[i+1]):
            return (a2+1) % 2
        return a2

# как мне сделать, чтобы при первой итерации выводился и первый символ(а1),
# а при последней - и последний(а3)? (помимо среднинных (а2))
def Convolutional_Fink_full_message_decoder(code: str, s=0) -> str:
    out = ''
    code = code
    for i in range(len(code)):
        message = Convolutional_Fink_decoder(code[i*2:i*2 + 5 + s * 8], s)
        if message == None: break
        else: out += str(message)
    return out

print(Convolutional_Fink_full_message_decoder('00010'))