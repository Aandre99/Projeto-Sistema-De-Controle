import sys

from windows.PrimaryWindow import Ui_PrimaryWindow
from windows.PeriodicWindow import Ui_PeriodicWindow
from windows.StepWindow import Ui_StepWindow
from graphics.PlotGraphic import MatplotlibWidget

from PyQt5.QtWidgets import QMainWindow, QApplication, QDesktopWidget

class Periodic(QMainWindow):

    def __init__(self, grafics, typ):

        super().__init__()
        self.ui = Ui_PeriodicWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Periodic Signal Parameters")
        self.graphic = grafics
        self.type_signal = typ
        self.ui.periodic_button.clicked.connect(self.build_signal)

    def set_type_signal(self, new_type):
        self.type_signal = new_type

    def build_signal(self):
        
        frequency = self.ui.lineEdit_freq.text()
        amplitude = self.ui.lineEdit_ampl.text()
        offset = self.ui.lineEdit_offs.text()

        self.graphic.show()
        self.graphic.periodic_signal(frequency, amplitude, offset, self.type_signal)

        self.ui.lineEdit_freq.clear()
        self.ui.lineEdit_ampl.clear()
        self.ui.lineEdit_offs.clear()
        self.hide()


class Step(QMainWindow):
    
    def __init__(self, grafics):
        super().__init__()
        self.ui = Ui_StepWindow()
        self.setWindowTitle("Step Signal Parameters")
        self.ui.setupUi(self)
        self.graphic = grafics
        self.ui.step_button.clicked.connect(self.plot_degrau)

    def plot_degrau(self):

        amplitude = self.ui.lineEdit_amplitude.text()

        self.graphic.show()
        self.graphic.degrau_signal(amplitude)
        self.ui.label_amplitude.clear()
        self.hide()

class MainW(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_PrimaryWindow()
        self.setWindowTitle("App Window")
        self.ui.setupUi(self)
        
        self.graphics = MatplotlibWidget(self)
        self.next_window1 = Step(self.graphics)
        self.next_window2 = Periodic(self.graphics, "Senoide")

        qtRectangle = self.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        self.move(qtRectangle.topLeft())

        self.ui.pushButton.clicked.connect(self.signal_choosed)
        self.show()

    def signal_choosed(self):
        
        peek = self.ui.comboBox_2.currentText()

        if peek == "Degrau":
            self.next_window1.show()
            self.hide()
        else:
            self.next_window2.set_type_signal(peek)
            self.next_window2.show()
            self.hide()

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = MainW()
    window.show()
    sys.exit(app.exec_())