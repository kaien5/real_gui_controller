# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'real_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1920, 1015)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.settings_mainWindow_frame = QtWidgets.QFrame(self.centralwidget)
        self.settings_mainWindow_frame.setGeometry(QtCore.QRect(30, 30, 241, 961))
        self.settings_mainWindow_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.settings_mainWindow_frame.setFrameShadow(QtWidgets.QFrame.Plain)
        self.settings_mainWindow_frame.setObjectName("settings_mainWindow_frame")
        self.injector_settings_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.injector_settings_button.setGeometry(QtCore.QRect(20, 80, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.injector_settings_button.setFont(font)
        self.injector_settings_button.setObjectName("injector_settings_button")
        self.settings_label = QtWidgets.QLabel(self.settings_mainWindow_frame)
        self.settings_label.setGeometry(QtCore.QRect(20, 20, 111, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.settings_label.setFont(font)
        self.settings_label.setObjectName("settings_label")
        self.microGC_settings_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.microGC_settings_button.setGeometry(QtCore.QRect(20, 160, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.microGC_settings_button.setFont(font)
        self.microGC_settings_button.setObjectName("microGC_settings_button")
        self.chiralMS_settings_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.chiralMS_settings_button.setGeometry(QtCore.QRect(20, 240, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.chiralMS_settings_button.setFont(font)
        self.chiralMS_settings_button.setObjectName("chiralMS_settings_button")
        self.start_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.start_button.setGeometry(QtCore.QRect(20, 880, 91, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 193, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(0, 193, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.start_button.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.stop_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(130, 880, 91, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(235, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(235, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.stop_button.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.stop_button.setFont(font)
        self.stop_button.setObjectName("stop_button")
        self.mass_spectrum = MplWidget(self.centralwidget)
        self.mass_spectrum.setGeometry(QtCore.QRect(290, 410, 811, 581))
        self.mass_spectrum.setObjectName("mass_spectrum")
        self.electron_image = MplWidget(self.centralwidget)
        self.electron_image.setGeometry(QtCore.QRect(1100, 410, 801, 581))
        self.electron_image.setObjectName("electron_image")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(300, 10, 1591, 401))
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.chromatogram1 = MplWidget(self.tab)
        self.chromatogram1.setGeometry(QtCore.QRect(0, 0, 1591, 381))
        self.chromatogram1.setObjectName("chromatogram1")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.chromatogram2 = MplWidget(self.tab_2)
        self.chromatogram2.setGeometry(QtCore.QRect(0, 0, 1591, 381))
        self.chromatogram2.setObjectName("chromatogram2")
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GC Chiral MS"))
        self.injector_settings_button.setText(_translate("MainWindow", "Injector"))
        self.settings_label.setText(_translate("MainWindow", "Settings"))
        self.microGC_settings_button.setText(_translate("MainWindow", "MicroGC"))
        self.chiralMS_settings_button.setText(_translate("MainWindow", "ChiralMS"))
        self.start_button.setText(_translate("MainWindow", "START"))
        self.stop_button.setText(_translate("MainWindow", "STOP"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Ch1 (FF)"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Ch2 (FF)"))
from mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
