# ------------------------------------------------------
# ---------------------- main.py -----------------------
# ------------------------------------------------------
from PyQt5.QtWidgets import*
from graphics.WindowGraphic import Ui_MainWindow
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

from scipy import signal
import numpy as np
import random
     
class MatplotlibWidget(QMainWindow):
    
    def __init__(self, backWindow):
        
        QMainWindow.__init__(self)

        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("Graphic of generated Signal")
        self.back = backWindow
        self.addToolBar(NavigationToolbar(self.ui.MlpWidget.canvas, self))

    def random_signal(self):

        fs = 500
        f = random.randint(1, 100)
        ts = 1/fs
        length_of_signal = 100
        t = np.linspace(0,1,length_of_signal)
        
        sinus_signal = np.sin(2*np.pi*f*t)

        self.ui.MlpWidget.canvas.axes.clear()
        self.ui.MlpWidget.canvas.axes.plot(t, sinus_signal)
        self.ui.MlpWidget.canvas.axes.legend(('Seno'),loc='upper right')
        self.ui.MlpWidget.canvas.axes.set_title('Sinus Signal')
        self.ui.MlpWidget.canvas.draw()
        
    def periodic_signal(self, frequency, amplitude, offset, type_signal):
        
        frequency = float(frequency)
        amplitude = float(amplitude)
        offset = float(offset)


        t = np.linspace(0,1,500)

        generated_signal = None

        if type_signal == "Senoide":
            generated_signal = amplitude * np.sin(2 * np.pi * frequency * t) + offset
        elif type_signal == "Serra":
            generated_signal = amplitude * signal.sawtooth(2 * np.pi * frequency * t) + offset
        elif type_signal == "Quadrada":
            generated_signal = amplitude * signal.square(2 * np.pi * frequency * t) + offset
       
        self.ui.MlpWidget.canvas.axes.clear()
        self.ui.MlpWidget.canvas.axes.plot(t,generated_signal, 0)
        self.ui.MlpWidget.canvas.axes.legend((f'{type_signal}'),loc='upper right')
        self.ui.MlpWidget.canvas.axes.set_title(f'{type_signal} Signal')
        self.ui.MlpWidget.canvas.draw()

    def degrau_signal(self, amplitude):
        
        t = np.linspace(0,1,100)
        ft = np.ones(t.shape[0]) * float(amplitude)

        self.ui.MlpWidget.canvas.axes.clear()
        self.ui.MlpWidget.canvas.axes.plot(t, ft)
        self.ui.MlpWidget.canvas.axes.legend(('Degrau'),loc='upper right')
        self.ui.MlpWidget.canvas.axes.set_title('Degrau Signal')
        self.ui.MlpWidget.canvas.draw()


    def closeEvent(self, event):
        
        self.back.show()
        self.hide()
        event.accept()