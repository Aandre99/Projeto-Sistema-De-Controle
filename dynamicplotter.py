# source https://github.com/ap--/python-live-plotting/blob/master/plot_pyqtgraph.py

from pyqtgraph.Qt import QtGui, QtCore
from PyQt6.QtWidgets import QApplication
import pyqtgraph as pg

import collections
import random
import time
import math
import numpy as np
from scipy.signal import sawtooth, square


class DynamicPlotter:
    def __init__(self, widget, sampleinterval=0.1, timewindow=10.0, size=(711, 451)):
        # Data stuff

        self.wave_type = "Senoide"
        self._interval = int(sampleinterval * 1000)

        self._bufsize = int(timewindow / sampleinterval)

        self.databuffer_1 = collections.deque([0.0] * self._bufsize, self._bufsize)
        self.databuffer_2 = collections.deque([0.0] * self._bufsize, self._bufsize)

        self.x_1 = np.linspace(-timewindow//2, timewindow//2, self._bufsize)
        self.y_1 = np.zeros(self._bufsize, dtype=float)

        self.x_2 = np.linspace(-timewindow//2, timewindow//2, self._bufsize)
        self.y_2 = np.zeros(self._bufsize, dtype=float)

        # variables

        self.amplitude = 10
        self.frequency = 0.5
        self.offset = 0

        self.max_value = 0
        self.min_value = 0
        self.max_periode = 0
        self.min_periode = 0

        # PyQtGraph stuff
        self.plt = pg.PlotWidget(widget)
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel("left", "amplitude", "V")
        self.plt.setLabel("bottom", "time", "s")
       
        # QTimer
        #if self.started:

        self.curve1 = self.plt.plot(self.x_1, self.y_1, pen=(255, 0, 0))
        self.curve2 = self.plt.plot(self.x_2, self.y_2, pen=(0, 0, 255))

        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateplot)
        self.timer.start(self._interval)

    def getdata(self):

        if self.wave_type == "Degrau":
            return self.step_wave()
        elif self.wave_type == "Senoide":
            return self.senoide_wave()
        elif self.wave_type == "Quadrada":
            return self.square_wave()
        elif self.wave_type == "Serra":
            return self.sawtooth_wave()

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
        return (
            5 * np.sin(time.time() * 0.3 * 2 * np.pi)
        )

    def updateplot(self):

        self.databuffer_1.append(self.getdata())
        self.databuffer_2.append(self.random_wave())

        self.y_1[:] = self.databuffer_1
        self.y_2[:] = self.databuffer_2

        self.curve1.setData(self.x_1, self.y_1)
        self.curve2.setData(self.x_2, self.y_2)

    def get_widget(self):
        return self.plt
