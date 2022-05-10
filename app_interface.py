from ast import arg
from PyQt6.QtWidgets import QMainWindow, QApplication
from interface import Ui_MainWindow
from dynamicplotter import DynamicPlotter
import sys
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

        self.ui.lineEdit_periodica_amplitude.setText("10")
        self.ui.lineEdit_periodica_frequencia.setText("0.5")
        self.ui.lineEdit_periodica_offset.setText("0")

        self.ui.lineEdit_aleatoria_AMax.setText("10")
        self.ui.lineEdit_aleatoria_AMin.setText("5")
        self.ui.lineEdit_aleatoria_PMin.setText("50")
        self.ui.lineEdit_aleatoria_PMax.setText("100")

        self.ui.comboBox_onda.currentTextChanged.connect(self.change_wave_widget)
        self.ui.pushButton_degrau.clicked.connect(self.setup_step_values)
        self.ui.pushButton_periodica.clicked.connect(self.setup_periodic_values)
        self.ui.pushButton_aleatoria.clicked.connect(self.setup_aleatory_values)
        self.ui.pushButton_window.clicked.connect(self.setup_window)

        self.server = RemoteControl(verbose=True)
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
    
    def setup_window(self):
        self.plotter.change_window(
            float(self.ui.lineEdit_janela_tam.text()),
            float(self.ui.lineEdit_janela_amost.text())
        )

if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = JanelaApp()
    window.show()
    sys.exit(app.exec())
