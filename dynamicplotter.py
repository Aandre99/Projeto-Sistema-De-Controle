# source https://github.com/ap--/python-live-plotting/blob/master/plot_pyqtgraph.py

from pyqtgraph.Qt import QtGui, QtCore
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg

import collections
import random
import time
import numpy as np
from scipy.signal import sawtooth, square


class DynamicPlotter:
    def __init__(self, buffer_ref, widget, sampleinterval=0.1, timewindow=10.0, size=(781, 501)):
        # Data stuff

        self.wave_type = "Senoide"
        self._interval = int(sampleinterval * 1000)

        self._bufsize = int(timewindow / sampleinterval)

        self.databuffer_1 = collections.deque([0.0] * self._bufsize, self._bufsize)
        #self.databuffer_2 = collections.deque([0.0] * self._bufsize, self._bufsize)

        self.x_1 = np.linspace(0, timewindow, self._bufsize)
        self.y_1 = np.zeros(self._bufsize, dtype=float)

        #self.x_2 = np.linspace(0, timewindow, self._bufsize)
        #self.y_2 = np.zeros(self._bufsize, dtype=float)

        # variables

        self.amplitude = 10
        self.frequency = 0.5
        self.offset = 0

        self.max_value = 10
        self.min_value = -5
        self.max_periode = 100
        self.min_periode = 50
        
        self.buffer_ref = buffer_ref

        # PyQtGraph stuff
        self.plt = pg.PlotWidget(widget)
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel("left", "amplitude", "V")
        self.plt.setLabel("bottom", "time", "s")
       
        # QTimer
        #if self.started:

        self.curve1 = self.plt.plot(self.x_1, self.y_1, pen=(255, 0, 0))
        #self.curve2 = self.plt.plot(self.x_2, self.y_2, pen=(0, 255, 0))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

        self.time_flag = time.time()
        self.t_prs = random.uniform(self.time_flag + self.min_periode, self.time_flag + self.max_periode)
        self.amplitude1 = random.uniform(self.min_value, self.max_value)

    def getdata(self):

        if self.wave_type == "Degrau":
            return self.step_wave()
        elif self.wave_type == "Senoide":
            return self.senoide_wave()
        elif self.wave_type == "Quadrada":
            return self.square_wave()
        elif self.wave_type == "Serra":
            return self.sawtooth_wave()
        elif self.wave_type == "Aleatoria":
            return self.random_wave()

    def senoide_wave(self): 
        return (
            self.amplitude * np.sin(time.time() * self.frequency * 2 * np.pi)
            + self.offset
        )

    def square_wave(self):
        return (
            self.amplitude * square(time.time() * self.frequency * 2 * np.pi)
            + self.offset
        )

    def sawtooth_wave(self):
        return (
            self.amplitude * sawtooth(time.time() * self.frequency * 2 * np.pi)
            + self.offset
        )

    def step_wave(self):
        return self.amplitude

    def random_wave(self):
        if self.time_flag >= self.t_prs:
                self.time_flag = time.time()
                self.t_prs = random.uniform(self.time_flag + self.min_periode, self.time_flag + self.max_periode)
                self.amplitude1 = random.uniform(self.min_value, self.max_value)
        else:
            self.time_flag = self.time_flag + 1
        new = self.amplitude1*square(2*np.pi*self.frequency*time.time()) + self.offset
        return new

    def updateplot(self):

        self.databuffer_1.append(self.getdata())
        #self.databuffer_2.append(6 * np.sin(time.time() * 0.7 * 2 * np.pi))

        self.y_1[:] = self.databuffer_1
        #self.y_2[:] = self.databuffer_2

        self.curve1.setData(self.x_1, self.y_1)
        #self.curve2.setData(self.x_2, self.y_2)

        #self.x_1 = self.x_1 + 0.005
        #self.x_2 = self.x_2 + 0.005

    def change_window(self, newSize, sampleRate):

        self._interval = int(sampleRate * 1000)
        self._bufsize = int(newSize / sampleRate)

        self.databuffer_1 = collections.deque([0.0] * self._bufsize, self._bufsize)
        self.databuffer_2 = collections.deque([0.0] * self._bufsize, self._bufsize)

        self.x_1 = np.linspace(0, newSize, self._bufsize)
        self.y_1 = np.zeros(self._bufsize, dtype=float)

        self.x_2 = np.linspace(0, newSize, self._bufsize)
        self.y_2 = np.zeros(self._bufsize, dtype=float)

        self.timer.start(self._interval)

    def get_widget(self):
        return self.plt
