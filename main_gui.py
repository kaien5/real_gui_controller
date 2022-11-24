# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_gui.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1896, 1084)
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
        self.start_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.start_button.setEnabled(False)
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
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        self.load_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.load_button.setEnabled(False)
        self.load_button.setGeometry(QtCore.QRect(130, 820, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.load_button.setFont(font)
        self.load_button.setObjectName("load_button")
        self.hvc_settings_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.hvc_settings_button.setGeometry(QtCore.QRect(20, 240, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.hvc_settings_button.setFont(font)
        self.hvc_settings_button.setObjectName("hvc_settings_button")
        self.motor_settings_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.motor_settings_button.setGeometry(QtCore.QRect(20, 320, 201, 61))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.motor_settings_button.setFont(font)
        self.motor_settings_button.setObjectName("motor_settings_button")
        self.enable_plots = QtWidgets.QCheckBox(self.settings_mainWindow_frame)
        self.enable_plots.setGeometry(QtCore.QRect(20, 400, 201, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.enable_plots.setFont(font)
        self.enable_plots.setObjectName("enable_plots")
        self.frame = QtWidgets.QFrame(self.settings_mainWindow_frame)
        self.frame.setGeometry(QtCore.QRect(20, 680, 201, 131))
        self.frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.ip_address_microGC = QtWidgets.QLineEdit(self.frame)
        self.ip_address_microGC.setGeometry(QtCore.QRect(100, 40, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ip_address_microGC.setFont(font)
        self.ip_address_microGC.setObjectName("ip_address_microGC")
        self.microGC_status = QtWidgets.QLabel(self.frame)
        self.microGC_status.setGeometry(QtCore.QRect(10, 100, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.microGC_status.setFont(font)
        self.microGC_status.setAlignment(QtCore.Qt.AlignCenter)
        self.microGC_status.setObjectName("microGC_status")
        self.ip_address_label = QtWidgets.QLabel(self.frame)
        self.ip_address_label.setGeometry(QtCore.QRect(10, 40, 81, 21))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.ip_address_label.setFont(font)
        self.ip_address_label.setObjectName("ip_address_label")
        self.microGC = QtWidgets.QLabel(self.frame)
        self.microGC.setGeometry(QtCore.QRect(10, 10, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.microGC.setFont(font)
        self.microGC.setAlignment(QtCore.Qt.AlignCenter)
        self.microGC.setObjectName("microGC")
        self.sequence_label = QtWidgets.QLabel(self.frame)
        self.sequence_label.setGeometry(QtCore.QRect(10, 70, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.sequence_label.setFont(font)
        self.sequence_label.setObjectName("sequence_label")
        self.sequence_number = QtWidgets.QSpinBox(self.frame)
        self.sequence_number.setEnabled(False)
        self.sequence_number.setGeometry(QtCore.QRect(149, 70, 42, 22))
        self.sequence_number.setMinimum(1)
        self.sequence_number.setObjectName("sequence_number")
        self.refresh_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.refresh_button.setGeometry(QtCore.QRect(20, 820, 91, 51))
        font = QtGui.QFont()
        font.setPointSize(13)
        font.setBold(True)
        font.setWeight(75)
        self.refresh_button.setFont(font)
        self.refresh_button.setObjectName("refresh_button")
        self.stop_button = QtWidgets.QPushButton(self.settings_mainWindow_frame)
        self.stop_button.setEnabled(False)
        self.stop_button.setGeometry(QtCore.QRect(130, 880, 91, 51))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(120, 120, 120))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.stop_button.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.stop_button.setFont(font)
        self.stop_button.setObjectName("stop_button")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(300, 10, 1591, 401))
        self.tabWidget.setObjectName("tabWidget")
        self.Ch1_FF_tab = QtWidgets.QWidget()
        self.Ch1_FF_tab.setObjectName("Ch1_FF_tab")
        self.Ch1_FF = MplWidget(self.Ch1_FF_tab)
        self.Ch1_FF.setEnabled(False)
        self.Ch1_FF.setGeometry(QtCore.QRect(0, 0, 1591, 381))
        self.Ch1_FF.setObjectName("Ch1_FF")
        self.reset_Ch1_FF = QtWidgets.QPushButton(self.Ch1_FF_tab)
        self.reset_Ch1_FF.setGeometry(QtCore.QRect(1480, 10, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.reset_Ch1_FF.setFont(font)
        self.reset_Ch1_FF.setObjectName("reset_Ch1_FF")
        self.tabWidget.addTab(self.Ch1_FF_tab, "")
        self.Ch2_FF_tab = QtWidgets.QWidget()
        self.Ch2_FF_tab.setObjectName("Ch2_FF_tab")
        self.Ch2_FF = MplWidget(self.Ch2_FF_tab)
        self.Ch2_FF.setEnabled(False)
        self.Ch2_FF.setGeometry(QtCore.QRect(0, 0, 1591, 381))
        self.Ch2_FF.setObjectName("Ch2_FF")
        self.reset_Ch2_FF = QtWidgets.QPushButton(self.Ch2_FF_tab)
        self.reset_Ch2_FF.setGeometry(QtCore.QRect(1480, 10, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.reset_Ch2_FF.setFont(font)
        self.reset_Ch2_FF.setObjectName("reset_Ch2_FF")
        self.tabWidget.addTab(self.Ch2_FF_tab, "")
        self.Ch2_BF_tab = QtWidgets.QWidget()
        self.Ch2_BF_tab.setObjectName("Ch2_BF_tab")
        self.Ch2_BF = MplWidget(self.Ch2_BF_tab)
        self.Ch2_BF.setEnabled(False)
        self.Ch2_BF.setGeometry(QtCore.QRect(0, 0, 1591, 381))
        self.Ch2_BF.setObjectName("Ch2_BF")
        self.reset_Ch2_BF = QtWidgets.QPushButton(self.Ch2_BF_tab)
        self.reset_Ch2_BF.setGeometry(QtCore.QRect(1480, 10, 93, 28))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.reset_Ch2_BF.setFont(font)
        self.reset_Ch2_BF.setObjectName("reset_Ch2_BF")
        self.tabWidget.addTab(self.Ch2_BF_tab, "")
        self.last_method = QtWidgets.QLabel(self.centralwidget)
        self.last_method.setGeometry(QtCore.QRect(960, 0, 271, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.last_method.setFont(font)
        self.last_method.setAlignment(QtCore.Qt.AlignCenter)
        self.last_method.setObjectName("last_method")
        self.tabWidget_2 = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_2.setGeometry(QtCore.QRect(300, 410, 1591, 581))
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tab_4 = QtWidgets.QWidget()
        self.tab_4.setObjectName("tab_4")
        self.electron_image = MplWidget(self.tab_4)
        self.electron_image.setEnabled(False)
        self.electron_image.setGeometry(QtCore.QRect(820, 0, 771, 581))
        self.electron_image.setObjectName("electron_image")
        self.mass_spectrum = MplWidget(self.tab_4)
        self.mass_spectrum.setEnabled(False)
        self.mass_spectrum.setGeometry(QtCore.QRect(-10, 0, 831, 581))
        self.mass_spectrum.setObjectName("mass_spectrum")
        self.tabWidget_2.addTab(self.tab_4, "")
        self.Table_tab = QtWidgets.QWidget()
        self.Table_tab.setObjectName("Table_tab")
        self.chromatogram_table = QtWidgets.QTableWidget(self.Table_tab)
        self.chromatogram_table.setEnabled(False)
        self.chromatogram_table.setGeometry(QtCore.QRect(180, 10, 1241, 531))
        self.chromatogram_table.setAutoFillBackground(True)
        self.chromatogram_table.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.chromatogram_table.setObjectName("chromatogram_table")
        self.chromatogram_table.setColumnCount(0)
        self.chromatogram_table.setRowCount(0)
        self.tabWidget_2.addTab(self.Table_tab, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menuBar = QtWidgets.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 1896, 26))
        self.menuBar.setObjectName("menuBar")
        self.menu_Open = QtWidgets.QMenu(self.menuBar)
        self.menu_Open.setObjectName("menu_Open")
        MainWindow.setMenuBar(self.menuBar)
        self.action_Open = QtWidgets.QAction(MainWindow)
        self.action_Open.setObjectName("action_Open")
        self.menu_Open.addAction(self.action_Open)
        self.menuBar.addAction(self.menu_Open.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(2)
        self.tabWidget_2.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "GC Chiral MS"))
        self.injector_settings_button.setText(_translate("MainWindow", "Injector"))
        self.settings_label.setText(_translate("MainWindow", "Settings"))
        self.microGC_settings_button.setText(_translate("MainWindow", "MicroGC"))
        self.start_button.setText(_translate("MainWindow", "START"))
        self.load_button.setText(_translate("MainWindow", "LOAD"))
        self.hvc_settings_button.setText(_translate("MainWindow", "Voltage control"))
        self.motor_settings_button.setText(_translate("MainWindow", "Motor Control"))
        self.enable_plots.setText(_translate("MainWindow", "Enable Plots"))
        self.ip_address_microGC.setText(_translate("MainWindow", "127.0.0.1"))
        self.microGC_status.setText(_translate("MainWindow", "Status unknown"))
        self.ip_address_label.setText(_translate("MainWindow", "IP Address:"))
        self.microGC.setText(_translate("MainWindow", "Micro GC"))
        self.refresh_button.setText(_translate("MainWindow", "Refresh"))
        self.stop_button.setText(_translate("MainWindow", "STOP"))
        self.reset_Ch1_FF.setText(_translate("MainWindow", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Ch1_FF_tab), _translate("MainWindow", "Ch1 (FF)"))
        self.reset_Ch2_FF.setText(_translate("MainWindow", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Ch2_FF_tab), _translate("MainWindow", "Ch2 (FF)"))
        self.reset_Ch2_BF.setText(_translate("MainWindow", "Reset"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Ch2_BF_tab), _translate("MainWindow", "Ch2 (BF)"))
        self.last_method.setText(_translate("MainWindow", "Method name"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.tab_4), _translate("MainWindow", "TOF spectrum and electron image"))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.Table_tab), _translate("MainWindow", "Table"))
        self.menu_Open.setTitle(_translate("MainWindow", "File"))
        self.action_Open.setText(_translate("MainWindow", "&Open"))
from mplwidget import MplWidget


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
