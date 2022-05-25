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
    def __init__(self, widget, sampleinterval=0.1, timewindow=20.0, size=(781, 501)):

        self.wave_type = "Senoide"
        self._interval = int(sampleinterval * 1000)

        self._bufsize = int(timewindow / sampleinterval)

        # Buffers

        self.databuffer_ref_IN = collections.deque([0.0] * self._bufsize, self._bufsize)
        self.databuffer_output1 = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )
        self.databuffer_output2 = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )
        self.databuffer_error = collections.deque([0.0] * self._bufsize, self._bufsize)
        self.databuffer_prop_error = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )
        self.databuffer_deriv_error = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )
        self.databuffer_integ_error = collections.deque(
            [0.0] * self._bufsize, self._bufsize
        )

        self.x = np.linspace(0, timewindow, self._bufsize)

        self.y_ref_IN = np.zeros(self._bufsize, dtype=float)
        self.y_out1 = np.zeros(self._bufsize, dtype=float)
        self.y_out2 = np.zeros(self._bufsize, dtype=float)
        self.y_error = np.zeros(self._bufsize, dtype=float)
        self.y_prop_error = np.zeros(self._bufsize, dtype=float)
        self.y_deriv_error = np.zeros(self._bufsize, dtype=float)
        self.y_integ_error = np.zeros(self._bufsize, dtype=float)

        self.type_loop = "Aberta"

        # Valores para os campos da interface

        self.amplitude = 10
        self.frequency = 0.5
        self.offset = 0

        self.max_value = 10
        self.min_value = -5
        self.max_periode = 100
        self.min_periode = 50
        self.current_ref_value = 0

        # Valores para gerenciar as entradas para os controladores

        self.P = 0.00001
        self.I = 0.00001
        self.D = 0.00001
        self.crtl = "P"
        self.error = 0
        self.prop_error = 0
        self.integ_error = 0
        self.deriv_error = 0

        self.saida = "Verde"
        self.current_time = 0
        self.N = 0

        # Configurações do plot

        self.plt = pg.PlotWidget(widget)

        self.plt.resize(*size)
        self.plt.showGrid(x=True, y=True)
        self.plt.setLabel("left", "amplitude", "V")
        self.plt.setLabel("bottom", "time", "s")

        self.curve_ref_IN = self.plt.plot(self.x, self.y_ref_IN, pen=(255, 255, 0))
        self.curve_out1 = self.plt.plot(self.x, self.y_out1, pen=(255, 0, 0))
        self.curve_out2 = self.plt.plot(self.x, self.y_out2, pen=(0, 255, 0))
        self.curve_error = self.plt.plot(self.x, self.y_error, pen=(0, 0, 255))
        self.curve_prop_error = self.plt.plot(
            self.x, self.y_prop_error, pen=(131, 111, 255)
        )
        self.curve_deriv_error = self.plt.plot(
            self.x, self.y_deriv_error, pen=(255, 69, 0)
        )
        self.curve_integ_error = self.plt.plot(
            self.x, self.y_integ_error, pen=(176, 224, 230)
        )

        # Configurações para esconder curvas do plot

        self.plots = {
            "b1": [0, self.curve_out1],
            "b2": [0, self.curve_out2],
            "refIN": [0, self.curve_ref_IN],
            "error": [0, self.curve_error],
            "Deriv": [0, self.curve_deriv_error],
            "Integ": [0, self.curve_integ_error],
            "Prop": [0, self.curve_prop_error],
        }

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

    def updateplot_communication(self, out1, out2, time):

        self.N += 1
        self.current_time = time
        self.current_ref_value = self.getdata(time)
        self.databuffer_ref_IN.append(self.current_ref_value)
        self.databuffer_output1.append(out1)
        self.databuffer_output2.append(out2)

        self.databuffer_error.append(self.error)
        self.databuffer_prop_error.append(self.prop_error)
        self.databuffer_deriv_error.append(self.deriv_error)
        self.databuffer_integ_error.append(self.integ_error)

        self.y_ref_IN[:] = self.databuffer_ref_IN
        self.y_out1[:] = self.databuffer_output1
        self.y_out2[:] = self.databuffer_output2

        self.y_error[:] = self.databuffer_error
        self.y_prop_error[:] = self.databuffer_prop_error
        self.y_deriv_error[:] = self.databuffer_deriv_error
        self.y_integ_error[:] = self.databuffer_integ_error

        self.curve_ref_IN.setData(self.x, self.y_ref_IN)
        self.curve_out1.setData(self.x, self.y_out1)
        self.curve_out2.setData(self.x, self.y_out2)

        self.curve_error.setData(self.x, self.y_error)
        self.curve_prop_error.setData(self.x, self.y_prop_error)
        self.curve_deriv_error.setData(self.x, self.y_deriv_error)
        self.curve_integ_error.setData(self.x, self.y_integ_error)

    def update_plot_curves(self, curve):

        self.plots[curve][0] += 1
        if self.plots[curve][0] % 2 == 1:
            self.plt.removeItem(self.plots[curve][1])
        else:
            self.plt.addItem(self.plots[curve][1])

    def get_ref_value(self, out2, controllers):

        if self.type_loop == "Aberta":
            return self.current_ref_value
        else:
            controllers[self.crtl].set_values(self.P, self.I, self.D)
            controllers[self.crtl].reference(self.current_ref_value)
            controllers[self.crtl].measured(out2)
            self.error = controllers[self.crtl].control()

            iae_error = controllers[self.crtl].IAE_error(self.N)
            ise_error = controllers[self.crtl].ISE_error(self.N)
            itae_error = controllers[self.crtl].ITAE_error(self.N, self.current_time)

            if self.N % 100 == 0:
                print(
                    f"IAE = {iae_error}, ISE = {ise_error}, ITAE = {itae_error}"
                )
            controllers[self.crtl].apply(self.error)

            if self.crtl != "P":
                self.prop_error, self.deriv_error, self.integ_error = controllers[
                    self.crtl
                ].get_components_erros()
            return self.error

    def get_widget(self):
        return self.plt
