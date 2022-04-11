# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PeriodicWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_PeriodicWindow(object):
    def setupUi(self, PeriodicWindow):
        PeriodicWindow.setObjectName("PeriodicWindow")
        PeriodicWindow.resize(668, 344)
        PeriodicWindow.setMinimumSize(QtCore.QSize(668, 344))
        PeriodicWindow.setMaximumSize(QtCore.QSize(668, 344))
        self.centralwidget = QtWidgets.QWidget(PeriodicWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame_green = QtWidgets.QFrame(self.centralwidget)
        self.frame_green.setGeometry(QtCore.QRect(0, 0, 121, 351))
        self.frame_green.setStyleSheet("background-color: rgb(156, 204, 152);")
        self.frame_green.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_green.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_green.setObjectName("frame_green")
        self.frame_white = QtWidgets.QFrame(self.centralwidget)
        self.frame_white.setGeometry(QtCore.QRect(119, -1, 551, 351))
        self.frame_white.setStyleSheet("background-color: rgb(250, 245, 245);")
        self.frame_white.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_white.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_white.setObjectName("frame_white")
        self.label_periodica = QtWidgets.QLabel(self.frame_white)
        self.label_periodica.setGeometry(QtCore.QRect(110, 50, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_periodica.setFont(font)
        self.label_periodica.setObjectName("label_periodica")
        self.formLayoutWidget = QtWidgets.QWidget(self.frame_white)
        self.formLayoutWidget.setGeometry(QtCore.QRect(140, 120, 286, 124))
        self.formLayoutWidget.setObjectName("formLayoutWidget")
        self.formLayout = QtWidgets.QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(12, 5, 62, 6)
        self.formLayout.setHorizontalSpacing(27)
        self.formLayout.setVerticalSpacing(17)
        self.formLayout.setObjectName("formLayout")
        self.label_frequency = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_frequency.setFont(font)
        self.label_frequency.setObjectName("label_frequency")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_frequency)
        self.lineEdit_freq = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_freq.setStyleSheet("QLineEdit{\n"
"border: 2px solid black;\n"
"border-radius: 20px;\n"
"background: white;\n"
"};")
        self.lineEdit_freq.setObjectName("lineEdit_freq")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineEdit_freq)
        self.label_amplitude = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_amplitude.setFont(font)
        self.label_amplitude.setObjectName("label_amplitude")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_amplitude)
        self.label_offset = QtWidgets.QLabel(self.formLayoutWidget)
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.label_offset.setFont(font)
        self.label_offset.setObjectName("label_offset")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_offset)
        self.lineEdit_ampl = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_ampl.setStyleSheet("QLineEdit{\n"
"border: 2px solid black;\n"
"border-radius: 20px;\n"
"background: white;\n"
"};")
        self.lineEdit_ampl.setObjectName("lineEdit_ampl")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineEdit_ampl)
        self.lineEdit_offs = QtWidgets.QLineEdit(self.formLayoutWidget)
        self.lineEdit_offs.setStyleSheet("QLineEdit{\n"
"border: 2px solid black;\n"
"border-radius: 20px;\n"
"background: white;\n"
"};")
        self.lineEdit_offs.setObjectName("lineEdit_offs")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.lineEdit_offs)
        self.periodic_button = QtWidgets.QPushButton(self.frame_white)
        self.periodic_button.setGeometry(QtCore.QRect(210, 280, 111, 41))
        self.periodic_button.setStyleSheet("QPushButton{\n"
"border: 2px solid black;\n"
"border-radius:10px;\n"
"}\n"
"QPushButton#periodica_bt:pressed {\n"
"    background-color: gray;\n"
"    color:white;\n"
"}")
        self.periodic_button.setObjectName("periodic_button")
        PeriodicWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PeriodicWindow)
        QtCore.QMetaObject.connectSlotsByName(PeriodicWindow)

    def retranslateUi(self, PeriodicWindow):
        _translate = QtCore.QCoreApplication.translate
        PeriodicWindow.setWindowTitle(_translate("PeriodicWindow", "MainWindow"))
        self.label_periodica.setText(_translate("PeriodicWindow", "Configurações Senoide"))
        self.label_frequency.setText(_translate("PeriodicWindow", "Frequência"))
        self.label_amplitude.setText(_translate("PeriodicWindow", "Amplitude"))
        self.label_offset.setText(_translate("PeriodicWindow", "Offset"))
        self.periodic_button.setText(_translate("PeriodicWindow", "Gerar Sinal"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    PeriodicWindow = QtWidgets.QMainWindow()
    ui = Ui_PeriodicWindow()
    ui.setupUi(PeriodicWindow)
    PeriodicWindow.show()
    sys.exit(app.exec_())