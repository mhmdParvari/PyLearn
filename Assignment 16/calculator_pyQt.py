import math
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('calculatorUi.ui')
        self.ui.show()
        self.number = 0
        self.decimal_flag = False
        self.decimal_maker = 10
        self.result = 0
        self.error_flag = False
        self.previous_operation = '+'
        self.current_operation = None
        self.ui.display.setReadOnly(True)
        self.ui.num0.clicked.connect(lambda:self.make_number(0))
        self.ui.num1.clicked.connect(lambda:self.make_number(1))
        self.ui.num2.clicked.connect(lambda:self.make_number(2))
        self.ui.num3.clicked.connect(lambda:self.make_number(3))
        self.ui.num4.clicked.connect(lambda:self.make_number(4))
        self.ui.num5.clicked.connect(lambda:self.make_number(5))
        self.ui.num6.clicked.connect(lambda:self.make_number(6))
        self.ui.num7.clicked.connect(lambda:self.make_number(7))
        self.ui.num8.clicked.connect(lambda:self.make_number(8))
        self.ui.num9.clicked.connect(lambda:self.make_number(9))
        self.ui.negate.clicked.connect(self.negate)
        self.ui.decimal_point.clicked.connect(self.decimal_point)
        self.ui.plus.clicked.connect(lambda:self.calculation('+'))
        self.ui.minus.clicked.connect(lambda:self.calculation('-'))
        self.ui.cross.clicked.connect(lambda:self.calculation('x'))
        self.ui.div.clicked.connect(lambda:self.calculation('÷'))
        self.ui.sin.clicked.connect(lambda:self.calculation('sin'))
        self.ui.cos.clicked.connect(lambda:self.calculation('cos'))
        self.ui.tan.clicked.connect(lambda:self.calculation('tan'))
        self.ui.cot.clicked.connect(lambda:self.calculation('cot'))
        self.ui.sqrt.clicked.connect(lambda:self.calculation('√'))
        self.ui.log10.clicked.connect(lambda:self.calculation('log₁₀'))
        self.ui.equlas.clicked.connect(self.print_result)
        self.ui.C.clicked.connect(self.clear)


    def append_to_text(self, _str):
        self.ui.display.setText(self.ui.display.toPlainText() + _str)

    def decimal_point(self):
        if not self.decimal_flag:
            self.decimal_flag = True
            if self.number == None:
                self.append_to_text('\n0.')
                self.number = 0
            else:
                self.append_to_text('0.' if self.number == 0 and not self.ui.display.toPlainText().endswith('0') else '.')

    def reset_number(self):
        self.number = 0
        self.decimal_flag = False
        self.decimal_maker = 10

    def negate(self):
        if self.number == 0 or self.number == None: return
        number = round(self.number, int(math.log10(self.decimal_maker))) #bcs of the infamous .1+.2 problem
        text = self.ui.display.toPlainText()
        sign_position = text.rfind(str(number)) if number > 0 else text.rfind(str(number))

        if text[sign_position] == '-':
            self.ui.display.setText(text[:sign_position] +  str(number*-1))
        else: 
            self.ui.display.setText(text[:sign_position] + str(number*-1))

        self.number *= -1


    def make_number(self,num):
        if self.number == None:
            self.number = 0
            self.append_to_text('\n')
        self.append_to_text(str(num))
        if self.number < 0: num *= -1
        if not self.decimal_flag:
            self.number = self.number * 10 + num
        else:
            self.number += num / self.decimal_maker
            self.decimal_maker *= 10
        
    def calculation(self,operator):
        if (self.previous_operation =='=' or self.error_flag) and self.number !=None:
            self.result = 0
            self.previous_operation = '+'
            
        if self.previous_operation == '+':
            self.result = self.result + self.number
        if self.previous_operation == '-':
            self.result = self.result - self.number
        if self.previous_operation == 'x':
            self.result = self.result * self.number
        if self.previous_operation == 'sin':
            self.result = math.sin(math.radians(self.result))
        if self.previous_operation == 'cos':
            self.result = math.cos(math.radians(self.result))
        if self.previous_operation == 'tan':
            self.result = math.tan(math.radians(self.result))
        if self.previous_operation == 'cot':
            self.result = 1 / math.tan(math.radians(self.result))
        self.error_flag = False
        try:
            if self.previous_operation == '÷':
                self.result = self.result / self.number
            if self.previous_operation == 'log₁₀':
                self.result = math.log10(self.result)
            if self.previous_operation == '√':
                self.result = math.sqrt(self.result)
        except ZeroDivisionError:
            self.append_to_text('\nCannot devide by zero')
            self.error_flag = True
        except ValueError:
            self.append_to_text('\nDomain error')
            self.error_flag = True

        self.previous_operation = operator
        self.reset_number()
        if self.previous_operation == '=' or self.error_flag: self.number = None
        
        if not self.error_flag:
            if operator == 'sin' or operator == 'cos' or operator == 'tan' or operator == 'cot' or operator == 'log₁₀' or operator == '√': 
                self.append_to_text('  ' + operator + '(' + str(self.result) + ')')
                self.print_result()
                return
            self.append_to_text(operator)

    def print_result(self):
        self.calculation('=')
        self.result = round(self.result, 10) #bcs of the infamous .1+.2 problem and also 1/3
        if not self.error_flag: self.append_to_text('\n'+ str(self.result) +'  ')

    def clear(self):
        self.ui.display.clear()
        self.reset_number()


app = QApplication([])
window = Window()
app.exec()