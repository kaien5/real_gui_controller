from PyQt5 import QtWidgets
from chiralMS_settings import Ui_chiralMS_settings
from hvc_controller import HvcController
from motor_controller import MotorController


class ChiralMsController:
    def __init__(self):
        self.window_motor = None
        self.window_hvc = None
        self.window_MS = QtWidgets.QMainWindow()
        self.ui_MS = Ui_chiralMS_settings()
        self.ui_MS.setupUi(self.window_MS)
        self.window_MS.show()

        # The buttons for opening the hvc and motor control windows
        self.ui_MS.voltage_control_button.clicked.connect(self.open_hvc)
        self.ui_MS.motor_control_button.clicked.connect(self.open_motor_control)

    # The motor control window
    def open_motor_control(self):
        self.window_motor = MotorController()

    # The high voltages control window
    def open_hvc(self):
        self.window_hvc = HvcController()
