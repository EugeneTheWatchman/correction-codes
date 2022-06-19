from random import sample
from functools import reduce

def generate_random_message(lenght: int, num_of_ones=None):
    if lenght == 0:
        return ''
    if isinstance(num_of_ones, int):  # шум
        if num_of_ones >= lenght:
            ones_positions = [i for i in range(lenght)]
        else:
            ones_positions = sample(range(lenght), num_of_ones)
    else:  # сообщение
        num_of_ones = int(lenght/2)
        ones_positions = sample(range(lenght), num_of_ones)
    message = [0 for i in range(lenght)]
    for pos in ones_positions:
        message[pos] = 1
    return reduce(lambda x, y: str(x) + str(y), message) # преобразование обратно в строку

def add_noise(message: str, noise: str):
    # Пока что эта проверка не нужна, т.к. на вход уже должны поступать сообщения равной длины
    # # Проверка для уравнивания длины сообщений (длина "noise" становится равной длине "message")
    if len(noise) > len(message):
        noise = noise[0:len(message)]
    else:
        noise += '0'*(len(message)-len(noise))

    new_message = ''
    for m, n in zip(message, noise):
        new_message += str((int(m)+int(n)) % 2)
    return new_message


# print(generate_random_message(1))

