from PyQt5 import QtWidgets
from motor import Ui_motor_control_settings


class MotorController:
    def __init__(self):
        self.window_motor = QtWidgets.QMainWindow()
        self.ui_motor = Ui_motor_control_settings()
        self.ui_motor.setupUi(self.window_motor)
        self.window_motor.show()
