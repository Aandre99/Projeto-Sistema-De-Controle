from ast import arg
from PyQt6.QtWidgets import QMainWindow, QApplication
from interface import Ui_MainWindow
from dynamicplotter import DynamicPlotter
import sys
import os
from PyQt6.QtCore import QThreadPool
from communication import RemoteControl


class JanelaApp(QMainWindow):
    def __init__(self):

        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.plotter = DynamicPlotter(self.ui.widget_ploter, 0.01, timewindow=10)
        self.graphWidget = self.plotter.get_widget()
        self.graphWidget.setObjectName("graphWidget")

        self.gain_times_flag = 0

        self.ui.frame_saida.setVisible(False)
        self.ui.stackedWidget_controladores.setVisible(False)
        self.ui.frame_controle.setVisible(False)
        self.ui.pushButton_controle.setVisible(False)

        self.ui.lineEdit_degrau_amplitude.setText("10")

        self.ui.lineEdit_periodica_amplitude.setText("10")
        self.ui.lineEdit_periodica_frequencia.setText("0.5")
        self.ui.lineEdit_periodica_offset.setText("0")

        self.ui.lineEdit_aleatoria_AMax.setText("10")
        self.ui.lineEdit_aleatoria_AMin.setText("5")
        self.ui.lineEdit_aleatoria_PMin.setText("50")
        self.ui.lineEdit_aleatoria_PMax.setText("100")

        self.ui.comboBox_onda.currentTextChanged.connect(self.change_wave_widget)
        self.ui.comboBox_control.currentTextChanged.connect(
            self.change_controller_widget
        )

        self.ui.pushButton_degrau.clicked.connect(self.setup_step_values)
        self.ui.pushButton_periodica.clicked.connect(self.setup_periodic_values)
        self.ui.pushButton_aleatoria.clicked.connect(self.setup_aleatory_values)
        self.ui.pushButton_controle.clicked.connect(self.set_control_values)

        self.ui.checkBox_bloco1.stateChanged.connect(
            lambda x: self.plotter.update_plot_curves("b1")
        )
        self.ui.checkBox_bloco2.stateChanged.connect(
            lambda x: self.plotter.update_plot_curves("b2")
        )
        self.ui.checkBox_referencia.stateChanged.connect(
            lambda x: self.plotter.update_plot_curves("refIN")
        )
        self.ui.checkBox_error.stateChanged.connect(
            lambda x: self.plotter.update_plot_curves("error")
        )
        self.ui.checkBox_2.stateChanged.connect(
            self.set_input_control_types
        )

        self.ui.comboBox_malha.currentTextChanged.connect(self.set_loop_type)
        self.ui.comboBox_saida.currentTextChanged.connect(self.set_output_control)

        self.server = RemoteControl(dynamicplotter=self.plotter, verbose=True)
        self.threadpool = QThreadPool()
        self.threadpool.start(self.server)

    def change_wave_widget(self, value):
        
        if value == "Degrau":
            self.plotter.wave_type = "Degrau"
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_degrau)
        elif value in ["Senoide", "Quadrada", "Serra"]:
            self.plotter.wave_type = value
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_senoide)
        else:
            self.plotter.wave_type = "Aleatoria"
            self.ui.stackedWidget.setCurrentWidget(self.ui.page_aleatoria)

    def change_controller_widget(self, value):

        self.plotter.crtl = value

        deriv = "Kd" if self.gain_times_flag % 2 == 0 else "Td"
        integ = "Ki" if self.gain_times_flag % 2 == 0 else "Ti"

        if value == "P":
            self.ui.stackedWidget_controladores.setCurrentWidget(self.ui.page_P)
        elif value in ["PI", "PD"]:
            if value == "PI":
                self.ui.label_pdpi.setText(integ)
            elif value == "PD":
                self.ui.label_pdpi.setText(deriv)
            self.ui.stackedWidget_controladores.setCurrentWidget(self.ui.page_PI)
        else:
            self.ui.stackedWidget_controladores.setCurrentWidget(self.ui.page_PID)

    def setup_step_values(self):
        self.plotter.amplitude = float(self.ui.lineEdit_degrau_amplitude.text())

    def setup_periodic_values(self):
        self.plotter.amplitude = float(self.ui.lineEdit_periodica_amplitude.text())
        self.plotter.frequency = float(self.ui.lineEdit_periodica_frequencia.text())
        self.plotter.offset = float(self.ui.lineEdit_periodica_offset.text())

    def setup_aleatory_values(self):
        self.plotter.max_periode = float(self.ui.lineEdit_aleatoria_PMax.text())
        self.plotter.min_periode = float(self.ui.lineEdit_aleatoria_PMin.text())
        self.plotter.max_value = float(self.ui.lineEdit_aleatoria_AMax.text())
        self.plotter.max_value = float(self.ui.lineEdit_aleatoria_AMin.text())

    def set_loop_type(self, value):

        visibleFlag = True if value == "Fechada" else False

        self.ui.frame_saida.setVisible(visibleFlag)
        self.ui.frame_controle.setVisible(visibleFlag)
        self.ui.pushButton_controle.setVisible(visibleFlag)
        self.ui.stackedWidget_controladores.setVisible(visibleFlag)
        self.plotter.type_loop = value

    def set_control_values(self):

        ctrl = self.ui.comboBox_control.currentText()
        flag = self.gain_times_flag % 2 == 0

        if ctrl == "P":
            self.plotter.P = float(self.ui.lineEdit_P.text())
        elif ctrl in ["PI", "PD"]:
            kp = float(self.ui.lineEdit_PIPD_kp.text())
            ki = float(self.ui.lineEdit_PIPD_ki.text())

            self.plotter.P = kp

            if ctrl == "PI":
                if flag:
                    self.plotter.I = float(ki)
                else:
                    self.plotter.I = kp / (ki)
            else:

                if flag:
                    self.plotter.D = float(ki)
                else:
                    self.plotter.D = kp * float(ki)
        else:

            kp = float(self.ui.lineEdit_PID_kp.text())
            ki = float(self.ui.lineEdit_PID_ki.text())
            kd = float(self.ui.lineEdit_PID_kd.text())

            self.plotter.P = kp

            if flag:
                self.plotter.I = ki
                self.plotter.D = kd
            else:
                self.plotter.I = kp / ki
                self.plotter.D = kp * kd

    def set_input_control_types(self):

        self.gain_times_flag += 1

        ctrl = self.ui.comboBox_control.currentText()

        deriv = "Kd" if self.gain_times_flag % 2 == 0 else "Td"
        integ = "Ki" if self.gain_times_flag % 2 == 0 else "Ti"

        if ctrl == "PI":
            self.ui.label_pdpi.setText(integ)
        elif ctrl == "PD":
            self.ui.label_pdpi.setText(deriv)
        elif ctrl == "PID":
            self.ui.label_15.setText(integ)
            self.ui.label_16.setText(deriv)

    def set_output_control(self, value):
        self.plotter.saida = value

    def closeEvent(self, event):
        os._exit(1)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = JanelaApp()
    window.show()
    sys.exit(app.exec())
