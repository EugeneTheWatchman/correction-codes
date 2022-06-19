from PyQt5.QtWidgets import QApplication, QLabel
from PyQt5.QtCore import Qt #, QBasicTimer, pyqtSignal
from PyQt5 import QtWidgets, QtCore, QtGui
#from PyQt5.QtGui import QPalette, QColor
import sys
# написанные мной библиотечки
import coders
import decoders
import random_generation
import convolutional_101_111_code as _111_101_code
import Hamming_7_4_code
import Hamming_15_11_code

class CloseEvent(QtWidgets.QWidget):

    def closeEvent(self, event):
        if self.parent != None:
            event.accept()
        else:
            reply = QtWidgets.QMessageBox.question(self, 'Сообщение',
                        "Вы точно хотите выйти?", QtWidgets.QMessageBox.Yes |
                        QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
            #reply.setText("текст")
            #reply.addButton("нет", QtWidgets.QMessageBox.NoRole)
            #reply.addButton("да", QtWidgets.QMessageBox.YesRole)

            if reply == QtWidgets.QMessageBox.Yes:
                event.accept()
            else:
                event.ignore()

class StatisticsWindow(CloseEvent):
    def __init__(self, parent=None):
        super(StatisticsWindow, self).__init__(parent, QtCore.Qt.Window)
        self.parent = parent
        self.setupUi()
        self.move(QtCore.QPoint(40,40))

    def setupUi(self):
        # тут будет один слой с labels с информацией о статистике
        main_layout = QtWidgets.QVBoxLayout()
        # исследуемый код
        self.researched_code = QLabel()
        # длина исследуемого сообщения
        self.message_len = QLabel()
        # кол-во ошибочных бит при передаче
        self.num_of_wrong_bits_in_channel = QLabel()
        # кол-во итераций
        self.iteration_amount = QLabel()
        # процент верно принятых
        self.correct_percentage_label = QLabel()

        main_layout.addWidget(self.researched_code)
        main_layout.addWidget(self.message_len)
        main_layout.addWidget(self.num_of_wrong_bits_in_channel)
        main_layout.addWidget(self.iteration_amount)
        main_layout.addWidget(self.correct_percentage_label)

        self.setLayout(main_layout)

        self.setWindowTitle('Окно со статистикой')


    def update_values(self, researched_code, message_len, num_of_wrong_bits_in_channel, num_of_bits_in_channel, iteration_amount, num_mistakes_bits, num_total_bits):
        # исследуемый код
        self.researched_code.setText(f'Исследуемый код: {researched_code}')
        # длина исследуемого сообщения
        self.message_len.setText(f'Длина исследуемого сообщения: {message_len}')
        # кол-во ошибочных бит при передаче
        self.num_of_wrong_bits_in_channel.setText(f'Количество ошибочных бит в канале передачи: {num_of_wrong_bits_in_channel} из {num_of_bits_in_channel} '
                                                f'({round(num_of_wrong_bits_in_channel/num_of_bits_in_channel*100,2)}%) ')
        # кол-во итераций
        #if isinstance(iteration_amount, str): self.iteration_amount.setText(iteration_amount)
        #else:
        self.iteration_amount.setText(f'Количество переданных сообщений: {iteration_amount}')
        # побитовая ошибка
        # for i in range(1,6):
        #     if num_mistakes_bits*10**(i-1) > num_total_bits:
        #         break
        mistake_percent = round(num_mistakes_bits/num_total_bits*100, 3)
        self.correct_percentage_label.setText(f'Остаточная ошибка на бит: {mistake_percent}% ({num_mistakes_bits} ошибок)')


class MainWindow(CloseEvent):
    items = ['Код Финка (1,2,2)', 'Свёрточный код (1,2,3)', 'Код Хэмминга (7,4)', 'Код Хэмминга (15,11)']
    # Важная особенность: при изменении значения combo box'a из кода, прикрепленная функция не активируется
        # а при измении значения TextEdit из кода - активируется
    # это на случай, если программа будет запущена в исполнения, до тыкания checkbox'a в блоке исходного сообщения.
        # т.е. это отражает начальное состояние программы
    input_message_random_generate = False
    noise_message_random_generate = False
    allowed_symbols = '01'

    def __init__(self, parent=None):
        self.parent = parent
        super(MainWindow, self).__init__(parent, QtCore.Qt.Window)
        self.setupUi()
        self.move(QtCore.QPoint(20,20))

        # изменеие цветов плохо работает со стилями
        #palette = self.palette()
        #palette.setColor(QPalette.HighlightedText, QColor(255,125,0))
        #palette.setColor(QPalette.Highlight, QColor(255,0,125))
        #self.setPalette(palette)

    def setupUi(self):
        #self.grid = QtWidgets.QGridLayout()
        #self.setStyleSheet('background-color: lightgray;')
        # желательно многопоточность ввести, чтобы приложуха не подвисала во время вычислений
        # и/или писать уведомление, что вычисления идут

        # крупyнее всё сделаю
        self.font_size = 19  # такая переменная нужна для установки корректного размера кнопок
        self.setStyleSheet(f'font-size: {self.font_size}px;')

        # генерация верхней полоски кнопок (можно в функцию вынести, кстати)
        if True:
            # тут немного всё поменялось, теперь сверху два блока будет
            top_block_layout = QtWidgets.QHBoxLayout()
            # рамка, позволяющая визуально отделить этот блок
            top_left_control_block = QtWidgets.QGroupBox()
            # макет расположения - горизонтальный (horizontal)
            top_control_block_layout = QtWidgets.QHBoxLayout()
            top_left_control_block.setLayout(top_control_block_layout)
            # выпадающий список
            combobox1 = QtWidgets.QComboBox()
            combobox1.addItems(self.items)
            combobox1.activated[str].connect(self.coder_changing_combobox)
            self.coder_changing_combobox(self.items[0])
            self.set_size_according_to_size_hint(combobox1)
            # кнопка рассчитать 1 раз
            button1 = QtWidgets.QPushButton('Рассчитать 1 раз')
            button1.setToolTip('Производит расчет модели')
            button1.clicked.connect(self.make_calculation_ones)
            self.set_size_according_to_size_hint(button1)
            # кнопка рассчитать 100(1000) раз
            button2 = QtWidgets.QPushButton('Рассчитать статистику')
            button2.setToolTip('Производит расчет модели выбранное число раз и затем выводит окно со статистикой')
            button2.clicked.connect(self.make_calculation_hundredfold)
            self.set_size_according_to_size_hint(button2)
                # отдельное окошко с результатом рассчетов всплывать должно

            label1 = QLabel('Выбор исследуемого кода: ')
            label1.setScaledContents(False)
            self.set_size_according_to_size_hint(label1)

            top_control_block_layout.addWidget(label1)
            top_control_block_layout.addWidget(combobox1)
            top_control_block_layout.addWidget(button1)

            ###
            if True:
                statistic_box = QtWidgets.QGroupBox()
                statistic_box_layout = QtWidgets.QGridLayout()
                statistic_box.setLayout(statistic_box_layout)
                #statistic_box_layout.setAlignment(Qt.AlignCenter)
                label3 = QLabel('Выбрано число итераций: 10')

                self.statistic_slider = QtWidgets.QSlider(Qt.Horizontal)
                #self.statistic_slider.setFocusPolicy(Qt.NoFocus)
                self.statistic_slider.setRange(10, 1000)
                self.statistic_slider.setPageStep(10)
                self.statistic_slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
                self.statistic_slider.setTickInterval(100)
                self.statistic_slider.setSingleStep(1)
                self.statistic_slider.valueChanged.connect(lambda value: label3.setText('Выбрано число итераций: ' + str(value)))

                label2 = QLabel('Выбор количества итераций для статистики: ')
                label2.setScaledContents(False)
                self.set_size_according_to_size_hint(label2)

                statistic_box_layout.addWidget(button2)
                statistic_box_layout.addWidget(label2)
                statistic_box_layout.addWidget(self.statistic_slider)
                statistic_box_layout.addWidget(label3)

            top_block_layout.addWidget(top_left_control_block)
            top_block_layout.addWidget(statistic_box)

            #self.set_size_according_to_size_hint(statistic_box)
            #self.set_size_according_to_size_hint(top_left_control_block)

        # генерация блока входного сообщения
        if True:
            input_message_block = QtWidgets.QGroupBox('Исходное сообщение')
            input_message_block.setStyleSheet('QGroupBox::title { margin-left: 18%;  margin-right: 18%;}')
            # макет расположения - горизонтальный (horizontal)
            input_message_block_layout = QtWidgets.QVBoxLayout()
            input_message_block.setLayout(input_message_block_layout)
            # поле с текстом
            self.input_message = QtWidgets.QTextEdit()
            #self.set_size_according_to_size_hint(self.input_message)
            # чекбокс о рандоме
            checkbox = QtWidgets.QCheckBox('Случайная генерация')
            checkbox.setToolTip('''Позволяет передавать случайно сгенерированное
сообщение, которое сгенерируется и выведется в это
текстовое окно после нажатия кнопки "рассчитать"''')
            checkbox.stateChanged.connect(self.change_input_message_random_mode)
            # а зачем на выбор длины сообщения ???
                # если чекбокс включен, то добавить выбор длины сообщения (или пусть прям в пустое поле вводят?)

            # self.input_message_lenght = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            # self.input_message_lenght.setRange(10, 99)  # случайные величины
            # self.input_message_lenght.valueChanged.connect(lambda value:
            #             self.label_input_message_lenght.setText('Установлена длина сообщения: '+str(value)))
            # #self.input_message_lenght = QtWidgets.QLineEdit()
            # #self.input_message_lenght.setValidator(QtGui.QIntValidator())
            # self.input_message_lenght.setHidden(True)

            self.input_message_lenght = QtWidgets.QLineEdit()
            self.input_message_lenght.setValidator(QtGui.QIntValidator())
            self.input_message_lenght.setText('0')
            self.input_message_lenght.setHidden(True)

            # эта штука приконнекчена к слайдеру self.input_message_lenght (line 100), нельзя убирать её просто так
            self.label_input_message_lenght = QLabel('Установите длину сообщения: ')
            self.label_input_message_lenght.setHidden(True)

            input_message_block_layout.addWidget(self.input_message)
            input_message_block_layout.addWidget(checkbox)
            input_message_block_layout.addWidget(self.label_input_message_lenght)
            input_message_block_layout.addWidget(self.input_message_lenght)
        # генерация блока кодера
        if True:
            coder_block = QtWidgets.QGroupBox('Закодированное сообщение')
            coder_block.setStyleSheet('QGroupBox::title { margin-left: 18%;  margin-right: 18%;}')
            # макет расположения - горизонтальный (horizontal)
            coder_block_layout = QtWidgets.QVBoxLayout()
            coder_block.setLayout(coder_block_layout)
            # вывод сообщения на кодере (поле с текстом неизменяемое)
            self.coder_message = QtWidgets.QTextEdit()
            self.coder_message.setReadOnly(True)
            # выбор дополнительных параметров кода (для сверточного кода - s: шаг кодирования/декодирования)
            #self.Fink_code_step =
            #slider = QtWidgets.QSlider(Qt.Horizontal)
            #slider.setFocusPolicy(Qt.StrongFocus)
            #slider.setTickPosition(QtWidgets.QSlider.TicksBothSides)
            #slider.setTickInterval(10)
            #slider.setSingleStep(1)
            coder_block_layout.addWidget(self.coder_message)
            #coder_block_layout.addWidget(slider)
        # генерация блока шума
        if True:
            noize_block = QtWidgets.QGroupBox('Вектор ошибок в канале передачи')
            noize_block.setStyleSheet('QGroupBox::title { margin-left: 18%;  margin-right: 18%;}')
            # макет расположения - горизонтальный (horizontal)
            noize_block_layout = QtWidgets.QVBoxLayout()
            noize_block.setLayout(noize_block_layout)

            # поле с текстом, куда можно ввести, желательно, только нужное кол-во бит (или лишние биты обрезать, а если нехватает - то дополнять нулями)
            self.noise_message = QtWidgets.QTextEdit()
            #self.noise_len = 1_000  # просто какое-то число, сколько нужно символов нужно еще определиться
            #self.noise_message.textChanged.connect(self.max_lenght_QTextEdit)
            #self.noise_message.setMaxLength(10)
            # нужно как-то разобраться как ограничивать число символов в ТЕКСТОВОМ ПОЛЕ

            # чекбокс о рандоме
            checkbox = QtWidgets.QCheckBox('Случайная генерация')
            checkbox.setToolTip('''Позволяет добавлять случайно сгенерированный
шум, который сгенерируется и выведется в это
текстовое окно после нажатия кнопки "рассчитать"''')
            checkbox.stateChanged.connect(self.change_noise_random_mode)

            # если чекбокс включен, дать возможность выбора колличества ошибочных бит
            self.noise_num_of_bits = QtWidgets.QLineEdit()
            self.noise_num_of_bits.setValidator(QtGui.QIntValidator())
            #self.noise_lenght_input.setInputMask('9999')
            self.noise_num_of_bits.setText('0')
            self.noise_num_of_bits.setHidden(True)

            self.label_noise_num_of_bits = QLabel('Введите количество ошибочных бит:')
            self.label_noise_num_of_bits.setHidden(True)


            noize_block_layout.addWidget(self.noise_message)
            noize_block_layout.addWidget(checkbox)
            noize_block_layout.addWidget(self.label_noise_num_of_bits)
            noize_block_layout.addWidget(self.noise_num_of_bits)
        # генерация блока декодера
        if True:
            decoder_block = QtWidgets.QGroupBox('Декодированное сообщение')
            decoder_block.setStyleSheet('QGroupBox::title { margin-left: 18%;  margin-right: 18%;}')
            # макет расположения - горизонтальный (horizontal)
            decoder_block_layout = QtWidgets.QVBoxLayout()
            decoder_block.setLayout(decoder_block_layout)
            # вывод сообщения на декодере (поле с текстом неизменяемое)
            self.decoder_message = QtWidgets.QTextEdit()
            self.decoder_message.setReadOnly(True)

            decoder_block_layout.addWidget(self.decoder_message)
        # генерация блока анализа
        if True:
            output_message_check_block = QtWidgets.QGroupBox('Анализ переданного сообщения')
            output_message_check_block.setStyleSheet('QGroupBox::title { margin-left: 18%;  margin-right: 18%;}')
            # макет расположения - горизонтальный (horizontal)
            output_message_check_block_layout = QtWidgets.QVBoxLayout()
            output_message_check_block.setLayout(output_message_check_block_layout)
            # вектор ошибок (неизменяемый)
            label1 = QLabel('Вектор ошибок:')
            label1.setToolTip('Показывает разницу между переданным сообщением и принятым')
            self.mistakes_message = QtWidgets.QTextEdit()
            self.mistakes_message.setReadOnly(True)
            # кол-во
            label2 = QLabel('Количество ошибок:')
            count_of_mistakes = QtWidgets.QLineEdit()
            count_of_mistakes.setReadOnly(True)
            # подключаем отображение кол-ва ошибок
            self.mistakes_message.textChanged.connect(lambda: self.count_num_of_mistakes(count_of_mistakes))

            output_message_check_block_layout.addWidget(label1)
            output_message_check_block_layout.addWidget(self.mistakes_message)
            output_message_check_block_layout.addWidget(label2)
            output_message_check_block_layout.addWidget(count_of_mistakes)

        # вспомогательный слой 1
        help_Hbox = QtWidgets.QHBoxLayout()
        # добавляем блоки слева направо
        help_Hbox.addWidget(input_message_block)
        help_Hbox.addWidget(coder_block)
        help_Hbox.addWidget(noize_block)
        help_Hbox.addWidget(decoder_block)
        help_Hbox.addWidget(output_message_check_block)
        # вот тут еще можно добавить соответствующее изображение со схемой

        # вспомогательный слой 2 (который и выставляем основным)
        help_Vbox = QtWidgets.QVBoxLayout()
        # добавляем слои сверху внихз
        help_Vbox.addLayout(top_block_layout)
        help_Vbox.addLayout(help_Hbox)
        self.setLayout(help_Vbox)

        self.setWindowTitle('Помехоустойчивое кодирование')

        # создание окна со статистикой
        self.make_statistics_window()

    def change_input_message_random_mode(self, state):
        # когда включен, должен располагать поле ввода сообщения в незименяемую форму (чтобы случайно не изменить)
        # print(state)
        if state != 0:  # галка стоит
            self.input_message.setReadOnly(True)
            self.input_message_lenght.setHidden(False)
            self.label_input_message_lenght.setHidden(False)
            self.input_message_random_generate = True
        else:   # галка не стоит
            self.input_message.setReadOnly(False)
            self.input_message_lenght.setHidden(True)
            self.label_input_message_lenght.setHidden(True)
            self.input_message_random_generate = False

    def change_noise_random_mode(self, state):
        # когда включен, должен располагать поле ввода шума в незименяемую форму (чтобы случайно не изменить)
        if state != 0:
            self.noise_message.setReadOnly(True)
            self.noise_num_of_bits.setHidden(False)
            self.label_noise_num_of_bits.setHidden(False)
            self.noise_message_random_generate = True
        else:
            self.noise_message.setReadOnly(False)
            self.noise_num_of_bits.setHidden(True)
            self.label_noise_num_of_bits.setHidden(True)
            self.noise_message_random_generate = False

    def coder_changing_combobox(self, text):
        # вызывается перед стартом программы 1 раз, чтобы назначить кодер и декодер по-умолчанию
        self.selected_code = text  # это нужно, чтобы показывать в окне со статистикой
        if text == self.items[0]:
            self.coder = coders.Convolutional_Fink_full_message_encoder
            self.decoder = decoders.Convolutional_Fink_full_message_decoder
        elif text == self.items[1]:
            self.coder = _111_101_code.Convolutional_101_111_full_message_encoder
            self.decoder = _111_101_code.Convolutional_101_111_full_message_decoder
        elif text == self.items[2]:
            self.coder = Hamming_7_4_code.Hamming_7_4_encoder
            self.decoder = Hamming_7_4_code.Hamming_7_4_decoder
        elif text == self.items[3]:
            self.coder = Hamming_15_11_code.Hamming_15_11_encoder
            self.decoder = Hamming_15_11_code.Hamming_15_11_decoder


    def make_calculation_ones(self):
        # s = 0
        if self.input_message_random_generate:  # если стоит галка на случайной генерации
            lenght_of_message = int((self.input_message_lenght.text())) #self.input_message_lenght.value()
            # нельзя передавать сообщение меньше 2-х символов:
            if lenght_of_message < 2:
                lenght_of_message = 2
            elif self.selected_code == self.items[2] and lenght_of_message > 4:
                lenght_of_message = 4
            elif self.selected_code == self.items[3] and lenght_of_message > 11:
                lenght_of_message = 11
            self.input_message_lenght.setText(str(lenght_of_message))
            # сгенерируем входное сообщение
            in_message = random_generation.generate_random_message(lenght_of_message)
            # выведем на экран далее, на выходе из блока if-else
        else:  # если не стоит галка на случайной генерации
            # читаем сообщение, которое хотим передать
                # и сразу же преобразуем в список (структура данных python)
            input_message = list(self.input_message.toPlainText())
            # проверка на легитимные символы:
            in_message = ''
            for i in input_message:
                if i in self.allowed_symbols:
                    in_message += i
                # добавляем в проверенное входное сообщение только легитимные символы

            lenght_of_message = len(in_message)
            if self.selected_code == self.items[2] and lenght_of_message > 4:
                lenght_of_message = 4
            elif self.selected_code == self.items[3] and lenght_of_message > 11:
                lenght_of_message = 11
            in_message = in_message[0:lenght_of_message]

        # выводим на экран проверенное/сгенерированное входное сообщение
        self.input_message.setPlainText(in_message)
        if len(in_message) == 0:
            self.coder_message.setPlainText('')
            self.decoder_message.setPlainText('')
            self.mistakes_message.setPlainText('')
            return

        # кодируем
        code_message = self.coder(in_message)#, s, True)
        self.coder_message.setPlainText(code_message)
        if self.noise_message_random_generate:  # если галочка включена
            # генерируем случайный шум, длиной как у code_message и с кол-вом ошибок указанным
            num_of_mistakes = self.noise_num_of_bits.text()
            if num_of_mistakes != '':
                num_of_mistakes = int(num_of_mistakes)
                if num_of_mistakes > len(code_message):
                    num_of_mistakes = len(code_message)
            else:
                num_of_mistakes = 0
            self.noise_num_of_bits.setText(str(num_of_mistakes))
            noise_message = random_generation.generate_random_message(len(code_message), num_of_mistakes)
        else:  # если галочка выключена
            noise_mes = self.noise_message.toPlainText()
            # проверка на легитимные символы:
            noise_message = ''
            for i in noise_mes:
                if i in self.allowed_symbols:
                    noise_message += i
                # добавляем в проверенное входное сообщение только легитимные символы
            # устанавливает длину "noise_message" равной длине "code_message"
            if len(noise_message) > len(code_message):
                noise_message = noise_message[0:len(code_message)]
            else:
                noise_message += '0'*(len(code_message)-len(noise_message))

        # выводим на экран проверенный/сгенерированный шум
        self.noise_message.setPlainText(noise_message)

        # добавляем шум к закодированному сообщению
        code_with_noise = random_generation.add_noise(code_message, noise_message)

        # декодируем код. сообщение с шумом и выводим на экран
        decoded_message = self.decoder(code_with_noise)#, s)
        self.decoder_message.setPlainText(decoded_message)

        # формируем вектор ошибок между исходным сообщением и декодированным и выводим на экран
        mistakes_vector = random_generation.add_noise(in_message, decoded_message)
        self.mistakes_message.setPlainText(mistakes_vector)

    def make_calculation_hundredfold(self):

        iterations = self.statistic_slider.value()
        #print('iterations = ', iterations)

        bit_mistakes_num = 0

        # читаем длину входного сообщения
        lenght_of_message = int(self.input_message_lenght.text()) #self.input_message_lenght.value()
        # нельзя передавать сообщение меньше 2-х символов:
        if lenght_of_message < 2:
            lenght_of_message = 2
        elif self.selected_code == self.items[2] and lenght_of_message > 4:
            lenght_of_message = 4
        elif self.selected_code == self.items[3] and lenght_of_message > 11:
            lenght_of_message = 11
        self.input_message_lenght.setText(str(lenght_of_message))

        # генерируем входное сообщение ( чисто для проверки кол-ва ошибок )
        in_message = random_generation.generate_random_message(lenght_of_message)
        # кодируем входное сообщение ( чисто для проверки кол-ва ошибок )
        code_message = self.coder(in_message)
        # считываем кол-во ошибок
        num_of_mistakes = self.noise_num_of_bits.text()
        if num_of_mistakes != '':
            num_of_mistakes = int(num_of_mistakes)
            if num_of_mistakes > len(code_message):
                num_of_mistakes = len(code_message)
        else:
            num_of_mistakes = 0
        self.noise_num_of_bits.setText(str(num_of_mistakes))

        if self.selected_code == self.items[0] or self.selected_code == self.items[1]:  # если выбрам сверточный код
            lenght_of_message *= iterations
            num_of_mistakes *= iterations
            iterations = 1

        for i in range(iterations):
            # генерируем входное сообщение
            in_message = random_generation.generate_random_message(lenght_of_message)
            # кодируем входное сообщение
            code_message = self.coder(in_message)#, s, True)

            # генерируем вектор ошибок (желательно только в самом сообщении, без старт-стопных символов)

            noise_message = random_generation.generate_random_message(len(code_message), num_of_mistakes)
            # прибавляем вектор ошибок к коду
            code_with_noise = random_generation.add_noise(code_message, noise_message)
            # декодируем код с ошибками
            decoded_message = self.decoder(code_with_noise)#, s)
            # сравниваем входное и выходное сообщения для получения битовой ошибки
            for in_mes, dec_mec in zip(in_message, decoded_message):
                if in_mes != dec_mec:  # если биты не равны, то
                    bit_mistakes_num += 1  # увеличиваем число ошибок на 1

        '''else:  # или передаем одно сообщение длиной iterations*lenght_of_message ( актуально для свёрточных кодов )
                # шаг кода Финка
                s = 0
                # генерируем входное сообщение

                lenght_of_message = lenght_of_message*iterations
                in_message = random_generation.generate_random_message(lenght_of_message)
                # кодируем входное сообщение
                code_message = self.coder(in_message, s, True)
                # считываем кол-во ошибок
                num_of_mistakes = int(self.noise_num_of_bits.text())*iterations
                # генерируем вектор ошибок
                noise_message = random_generation.generate_random_message(len(code_message), num_of_mistakes)
                # прибавляем вектор ошибок к коду
                code_with_noise = random_generation.add_noise(code_message, noise_message)
                # декодируем код с ошибками
                decoded_message = self.decoder(code_with_noise, s)
                # сравниваем входное и выходное сообщения для получения битовой ошибки
                for in_mes, dec_mec in zip(in_message, decoded_message):
                    if in_mes != dec_mec:  # если биты не равны, то
                        bit_mistakes_num += 1  # увеличиваем число ошибок на 1
                iterations = 1'''

        # общее кол-во переданных бит
        total_bits = iterations*lenght_of_message
        self.child.update_values(self.selected_code, lenght_of_message, num_of_mistakes,
                                 len(code_message), iterations, bit_mistakes_num, total_bits)
                                                                            # перевод в проценты
        self.child.show()

    def make_statistics_window(self):
        # как тебя закрыть, сука?
        self.child = StatisticsWindow(self)
        # self.child.show()
        # self.child.hide()

    # аккуратно, эта функция изменяет объект!
    def set_size_according_to_size_hint(self, obj):
        # print(obj.sizeHint()*2)
        obj.setFixedSize(obj.sizeHint()*self.font_size/16)

    # def max_lenght_QTextEdit(self):
    #     text = self.noise_message.toPlainText()
    #     if len(text) > self.noise_len:
    #         self.noise_message.textCursor().deletePreviousChar()

    def count_num_of_mistakes(self, QLineEdit):
        sum = 0
        for i in self.mistakes_message.toPlainText():
            sum += int(i)
        QLineEdit.setText(str(sum))



if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    win = MainWindow()
    win.show()
    sys.exit(app.exec_())
