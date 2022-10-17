# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'motor_control_settings.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_motor_control_settings(object):
    def setupUi(self, motor_control_settings):
        motor_control_settings.setObjectName("motor_control_settings")
        motor_control_settings.resize(641, 275)
        self.centralwidget = QtWidgets.QWidget(motor_control_settings)
        self.centralwidget.setObjectName("centralwidget")
        self.controller_serial_number_frame = QtWidgets.QFrame(self.centralwidget)
        self.controller_serial_number_frame.setGeometry(QtCore.QRect(10, 10, 361, 51))
        self.controller_serial_number_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.controller_serial_number_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controller_serial_number_frame.setObjectName("controller_serial_number_frame")
        self.controller_spinbox = QtWidgets.QSpinBox(self.controller_serial_number_frame)
        self.controller_spinbox.setGeometry(QtCore.QRect(10, 20, 181, 22))
        self.controller_spinbox.setObjectName("controller_spinbox")
        self.controller_label = QtWidgets.QLabel(self.controller_serial_number_frame)
        self.controller_label.setGeometry(QtCore.QRect(10, 0, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.controller_label.setFont(font)
        self.controller_label.setObjectName("controller_label")
        self.serial_number_line = QtWidgets.QLineEdit(self.controller_serial_number_frame)
        self.serial_number_line.setGeometry(QtCore.QRect(210, 20, 71, 21))
        self.serial_number_line.setObjectName("serial_number_line")
        self.serial_number_label = QtWidgets.QLabel(self.controller_serial_number_frame)
        self.serial_number_label.setGeometry(QtCore.QRect(210, 0, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.serial_number_label.setFont(font)
        self.serial_number_label.setObjectName("serial_number_label")
        self.refresh_button = QtWidgets.QPushButton(self.controller_serial_number_frame)
        self.refresh_button.setGeometry(QtCore.QRect(300, 20, 51, 21))
        self.refresh_button.setObjectName("refresh_button")
        self.controls_frame = QtWidgets.QFrame(self.centralwidget)
        self.controls_frame.setGeometry(QtCore.QRect(10, 70, 361, 191))
        self.controls_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.controls_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.controls_frame.setObjectName("controls_frame")
        self.left_button = QtWidgets.QPushButton(self.controls_frame)
        self.left_button.setGeometry(QtCore.QRect(10, 10, 41, 31))
        self.left_button.setObjectName("left_button")
        self.stop_button = QtWidgets.QPushButton(self.controls_frame)
        self.stop_button.setGeometry(QtCore.QRect(60, 10, 41, 31))
        self.stop_button.setObjectName("stop_button")
        self.right_button = QtWidgets.QPushButton(self.controls_frame)
        self.right_button.setGeometry(QtCore.QRect(110, 10, 41, 31))
        self.right_button.setObjectName("right_button")
        self.home_button = QtWidgets.QPushButton(self.controls_frame)
        self.home_button.setGeometry(QtCore.QRect(210, 10, 41, 31))
        self.home_button.setObjectName("home_button")
        self.null_button = QtWidgets.QPushButton(self.controls_frame)
        self.null_button.setGeometry(QtCore.QRect(260, 10, 41, 31))
        self.null_button.setObjectName("null_button")
        self.exit_button = QtWidgets.QPushButton(self.controls_frame)
        self.exit_button.setGeometry(QtCore.QRect(310, 10, 41, 31))
        self.exit_button.setObjectName("exit_button")
        self.position_label = QtWidgets.QLabel(self.controls_frame)
        self.position_label.setGeometry(QtCore.QRect(10, 63, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.position_label.setFont(font)
        self.position_label.setObjectName("position_label")
        self.position_line = QtWidgets.QLineEdit(self.controls_frame)
        self.position_line.setGeometry(QtCore.QRect(10, 80, 101, 20))
        self.position_line.setObjectName("position_line")
        self.uposition_line = QtWidgets.QLineEdit(self.controls_frame)
        self.uposition_line.setGeometry(QtCore.QRect(120, 80, 61, 20))
        self.uposition_line.setObjectName("uposition_line")
        self.uposition_label = QtWidgets.QLabel(self.controls_frame)
        self.uposition_label.setGeometry(QtCore.QRect(120, 63, 61, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.uposition_label.setFont(font)
        self.uposition_label.setObjectName("uposition_label")
        self.unit_spinbox = QtWidgets.QSpinBox(self.controls_frame)
        self.unit_spinbox.setGeometry(QtCore.QRect(210, 80, 91, 20))
        self.unit_spinbox.setObjectName("unit_spinbox")
        self.unit_label = QtWidgets.QLabel(self.controls_frame)
        self.unit_label.setGeometry(QtCore.QRect(210, 63, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.unit_label.setFont(font)
        self.unit_label.setObjectName("unit_label")
        self.absolute_position_spinbox = QtWidgets.QSpinBox(self.controls_frame)
        self.absolute_position_spinbox.setGeometry(QtCore.QRect(10, 120, 101, 22))
        self.absolute_position_spinbox.setObjectName("absolute_position_spinbox")
        self.relative_position_spinbox = QtWidgets.QSpinBox(self.controls_frame)
        self.relative_position_spinbox.setGeometry(QtCore.QRect(10, 150, 101, 22))
        self.relative_position_spinbox.setObjectName("relative_position_spinbox")
        self.absolute_uposition_spinbox = QtWidgets.QSpinBox(self.controls_frame)
        self.absolute_uposition_spinbox.setGeometry(QtCore.QRect(120, 120, 61, 22))
        self.absolute_uposition_spinbox.setObjectName("absolute_uposition_spinbox")
        self.relative_uposition_spinbox = QtWidgets.QSpinBox(self.controls_frame)
        self.relative_uposition_spinbox.setGeometry(QtCore.QRect(120, 150, 61, 22))
        self.relative_uposition_spinbox.setObjectName("relative_uposition_spinbox")
        self.move_absolute_button = QtWidgets.QPushButton(self.controls_frame)
        self.move_absolute_button.setGeometry(QtCore.QRect(210, 120, 91, 23))
        self.move_absolute_button.setObjectName("move_absolute_button")
        self.move_relative_button = QtWidgets.QPushButton(self.controls_frame)
        self.move_relative_button.setGeometry(QtCore.QRect(210, 150, 91, 23))
        self.move_relative_button.setObjectName("move_relative_button")
        self.status_frame = QtWidgets.QFrame(self.centralwidget)
        self.status_frame.setGeometry(QtCore.QRect(380, 10, 251, 251))
        self.status_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.status_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.status_frame.setObjectName("status_frame")
        self.vcts_frame = QtWidgets.QFrame(self.status_frame)
        self.vcts_frame.setGeometry(QtCore.QRect(10, 20, 111, 181))
        self.vcts_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.vcts_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.vcts_frame.setObjectName("vcts_frame")
        self.voltage_label = QtWidgets.QLabel(self.vcts_frame)
        self.voltage_label.setGeometry(QtCore.QRect(10, 3, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.voltage_label.setFont(font)
        self.voltage_label.setObjectName("voltage_label")
        self.voltage_line = QtWidgets.QLineEdit(self.vcts_frame)
        self.voltage_line.setGeometry(QtCore.QRect(10, 20, 91, 20))
        self.voltage_line.setObjectName("voltage_line")
        self.current_line = QtWidgets.QLineEdit(self.vcts_frame)
        self.current_line.setGeometry(QtCore.QRect(10, 60, 91, 20))
        self.current_line.setObjectName("current_line")
        self.current_label = QtWidgets.QLabel(self.vcts_frame)
        self.current_label.setGeometry(QtCore.QRect(10, 40, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.current_label.setFont(font)
        self.current_label.setObjectName("current_label")
        self.temperature_line = QtWidgets.QLineEdit(self.vcts_frame)
        self.temperature_line.setGeometry(QtCore.QRect(10, 100, 91, 20))
        self.temperature_line.setObjectName("temperature_line")
        self.temperatur_label = QtWidgets.QLabel(self.vcts_frame)
        self.temperatur_label.setGeometry(QtCore.QRect(10, 80, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.temperatur_label.setFont(font)
        self.temperatur_label.setObjectName("temperatur_label")
        self.speed_line = QtWidgets.QLineEdit(self.vcts_frame)
        self.speed_line.setGeometry(QtCore.QRect(10, 140, 91, 20))
        self.speed_line.setObjectName("speed_line")
        self.speed_label = QtWidgets.QLabel(self.vcts_frame)
        self.speed_label.setGeometry(QtCore.QRect(10, 120, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.speed_label.setFont(font)
        self.speed_label.setObjectName("speed_label")
        self.status_label = QtWidgets.QLabel(self.status_frame)
        self.status_label.setGeometry(QtCore.QRect(10, 0, 41, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.status_label.setFont(font)
        self.status_label.setObjectName("status_label")
        self.mada_frame = QtWidgets.QFrame(self.status_frame)
        self.mada_frame.setGeometry(QtCore.QRect(130, 20, 111, 181))
        self.mada_frame.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.mada_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.mada_frame.setObjectName("mada_frame")
        self.move_speed_label = QtWidgets.QLabel(self.mada_frame)
        self.move_speed_label.setGeometry(QtCore.QRect(10, 3, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.move_speed_label.setFont(font)
        self.move_speed_label.setObjectName("move_speed_label")
        self.move_speed_line = QtWidgets.QLineEdit(self.mada_frame)
        self.move_speed_line.setGeometry(QtCore.QRect(10, 20, 91, 20))
        self.move_speed_line.setObjectName("move_speed_line")
        self.acceleration_line = QtWidgets.QLineEdit(self.mada_frame)
        self.acceleration_line.setGeometry(QtCore.QRect(10, 60, 91, 20))
        self.acceleration_line.setObjectName("acceleration_line")
        self.acceleration_label = QtWidgets.QLabel(self.mada_frame)
        self.acceleration_label.setGeometry(QtCore.QRect(10, 40, 71, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.acceleration_label.setFont(font)
        self.acceleration_label.setObjectName("acceleration_label")
        self.deceleration_line = QtWidgets.QLineEdit(self.mada_frame)
        self.deceleration_line.setGeometry(QtCore.QRect(10, 100, 91, 20))
        self.deceleration_line.setObjectName("deceleration_line")
        self.deceleration_label = QtWidgets.QLabel(self.mada_frame)
        self.deceleration_label.setGeometry(QtCore.QRect(10, 80, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.deceleration_label.setFont(font)
        self.deceleration_label.setObjectName("deceleration_label")
        self.antiplayline = QtWidgets.QLineEdit(self.mada_frame)
        self.antiplayline.setGeometry(QtCore.QRect(10, 140, 91, 20))
        self.antiplayline.setObjectName("antiplayline")
        self.antiplay_speed = QtWidgets.QLabel(self.mada_frame)
        self.antiplay_speed.setGeometry(QtCore.QRect(10, 120, 81, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.antiplay_speed.setFont(font)
        self.antiplay_speed.setObjectName("antiplay_speed")
        self.get_button = QtWidgets.QPushButton(self.status_frame)
        self.get_button.setGeometry(QtCore.QRect(130, 212, 51, 31))
        self.get_button.setObjectName("get_button")
        self.set_button = QtWidgets.QPushButton(self.status_frame)
        self.set_button.setGeometry(QtCore.QRect(190, 212, 51, 31))
        self.set_button.setObjectName("set_button")
        motor_control_settings.setCentralWidget(self.centralwidget)

        self.retranslateUi(motor_control_settings)
        QtCore.QMetaObject.connectSlotsByName(motor_control_settings)

    def retranslateUi(self, motor_control_settings):
        _translate = QtCore.QCoreApplication.translate
        motor_control_settings.setWindowTitle(_translate("motor_control_settings", "Motor Control"))
        self.controller_label.setText(_translate("motor_control_settings", "Controller"))
        self.serial_number_label.setText(_translate("motor_control_settings", "Serial number"))
        self.refresh_button.setText(_translate("motor_control_settings", "Refresh"))
        self.left_button.setText(_translate("motor_control_settings", "Left"))
        self.stop_button.setText(_translate("motor_control_settings", "Stop"))
        self.right_button.setText(_translate("motor_control_settings", "Right"))
        self.home_button.setText(_translate("motor_control_settings", "Home"))
        self.null_button.setText(_translate("motor_control_settings", "0"))
        self.exit_button.setText(_translate("motor_control_settings", "Exit"))
        self.position_label.setText(_translate("motor_control_settings", "Position"))
        self.position_line.setText(_translate("motor_control_settings", "175"))
        self.uposition_line.setText(_translate("motor_control_settings", "0"))
        self.uposition_label.setText(_translate("motor_control_settings", "uPosition"))
        self.unit_label.setText(_translate("motor_control_settings", "Unit"))
        self.move_absolute_button.setText(_translate("motor_control_settings", "Move absolute"))
        self.move_relative_button.setText(_translate("motor_control_settings", "Move relative"))
        self.voltage_label.setText(_translate("motor_control_settings", "Voltage"))
        self.current_label.setText(_translate("motor_control_settings", "Current"))
        self.temperatur_label.setText(_translate("motor_control_settings", "Temperature"))
        self.speed_label.setText(_translate("motor_control_settings", "Speed"))
        self.status_label.setText(_translate("motor_control_settings", "Status"))
        self.move_speed_label.setText(_translate("motor_control_settings", "Move speed"))
        self.acceleration_label.setText(_translate("motor_control_settings", "Acceleration"))
        self.deceleration_label.setText(_translate("motor_control_settings", "Deceleration"))
        self.antiplay_speed.setText(_translate("motor_control_settings", "Antiplay speed"))
        self.get_button.setText(_translate("motor_control_settings", "Get"))
        self.set_button.setText(_translate("motor_control_settings", "Set"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    motor_control_settings = QtWidgets.QMainWindow()
    ui = Ui_motor_control_settings()
    ui.setupUi(motor_control_settings)
    motor_control_settings.show()
    sys.exit(app.exec_())
