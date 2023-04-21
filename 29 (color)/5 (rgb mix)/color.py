from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import *

color = [127,127,127]
class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = uic.loadUi('color.ui')
        self.ui.show()
        font = QWidget.font(self.ui.display)
        font.setPointSize(14)
        self.ui.display.setFont(font)
        self.ui.display.setText(f'     RGB {tuple(color)}')
        self.ui.display.setStyleSheet(f'background-color: rgb{tuple(color)}')

        self.ui.Rslider.setRange(0,255)
        self.ui.Gslider.setRange(0,255)
        self.ui.Bslider.setRange(0,255)

        self.ui.Rslider.setValue(127)
        self.ui.Gslider.setValue(127)
        self.ui.Bslider.setValue(127)

        self.ui.Rslider.valueChanged.connect(lambda val: self.red(val))
        self.ui.Gslider.valueChanged.connect(lambda val: self.green(val))
        self.ui.Bslider.valueChanged.connect(lambda val: self.blue(val))

    def red(self, value):
        color[0] = value
        self.ui.display.setStyleSheet(f'background-color: rgb{tuple(color)}')
        self.ui.display.setText(f'     RGB {tuple(color)}')
        
    def green(self, value):
        color[1] = value
        self.ui.display.setStyleSheet(f'background-color: rgb{tuple(color)}')
        self.ui.display.setText(f'     RGB {tuple(color)}')

    def blue(self, value):
        color[2] = value
        self.ui.display.setStyleSheet(f'background-color: rgb{tuple(color)}')
        self.ui.display.setText(f'     RGB {tuple(color)}')

    
app = QApplication([])
window = Window()
app.exec()
