# source https://github.com/ap--/python-live-plotting/blob/master/plot_pyqtgraph.py

from pkgutil import get_data
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
    def __init__(self, widget, sampleinterval=0.1, timewindow=10.0, size=(781, 501)):

        self.wave_type = "Senoide"
        self._interval = int(sampleinterval * 1000)

        self._bufsize = int(timewindow / sampleinterval)

        self.databuffer_ref = collections.deque([0.0] * self._bufsize, self._bufsize)
        self.databuffer_output1 = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )
        self.databuffer_output2 = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )

        self.x = np.linspace(0, timewindow, self._bufsize)

        self.y_ref = np.zeros(self._bufsize, dtype=float)
        self.y_out1 = np.zeros(self._bufsize, dtype=float)
        self.y_out2 = np.zeros(self._bufsize, dtype=float)

        self.amplitude = 10
        self.frequency = 0.5
        self.offset = 0

        self.max_value = 10
        self.min_value = -5
        self.max_periode = 100
        self.min_periode = 50

        self.current_ref_value = 0

        self.plt = pg.PlotWidget(widget)
        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel("left", "amplitude", "V")
        self.plt.setLabel("bottom", "time", "s")

        self.curve_ref = self.plt.plot(self.x, self.y_ref, pen=(255, 0, 0))
        self.curve_out1 = self.plt.plot(self.x, self.y_out1, pen=(0, 255, 0))
        self.curve_out2 = self.plt.plot(self.x, self.y_out2, pen=(0, 0, 255))

        self.time_flag = time.time()
        self.t_prs = random.uniform(
            self.time_flag + self.min_periode, self.time_flag + self.max_periode
        )
        self.amplitude1 = random.uniform(self.min_value, self.max_value)

    def getdata(self, t):

        if self.wave_type == "Degrau":
            return self.step_wave(t)
        elif self.wave_type == "Senoide":
            return self.senoide_wave(t)
        elif self.wave_type == "Quadrada":
            return self.square_wave(t)
        elif self.wave_type == "Serra":
            return self.sawtooth_wave(t)
        elif self.wave_type == "Aleatoria":
            return self.random_wave(t)

    def senoide_wave(self, t):
        return self.amplitude * np.sin(t * self.frequency * 2 * np.pi) + self.offset

    def square_wave(self, t):
        return self.amplitude * square(t * self.frequency * 2 * np.pi) + self.offset

    def sawtooth_wave(self, t):
        return self.amplitude * sawtooth(t * self.frequency * 2 * np.pi) + self.offset

    def step_wave(self, t):
        return self.amplitude

    def random_wave(self, t):
        if self.time_flag >= self.t_prs:
            self.time_flag = t
            self.t_prs = random.uniform(
                self.time_flag + self.min_periode, self.time_flag + self.max_periode
            )
            self.amplitude1 = random.uniform(self.min_value, self.max_value)
        else:
            self.time_flag = self.time_flag + 1
        new = self.amplitude1
        return new

    def updateplot_communication(self, ref, out1, out2, time):

        self.current_ref_value = self.getdata(time)
        self.databuffer_ref.append(self.current_ref_value)
        self.databuffer_output1.append(out1)
        self.databuffer_output2.append(out2)

        self.y_ref[:] = self.databuffer_ref
        self.y_out1[:] = self.databuffer_output1
        self.y_out2[:] = self.databuffer_output2

        self.curve_ref.setData(self.x, self.y_ref)
        self.curve_out1.setData(self.x, self.y_out1)
        self.curve_out2.setData(self.x, self.y_out2)

    def get_ref_value(self):
        return self.current_ref_value

    def get_widget(self):
        return self.plt
