from PyQt5 import QtWidgets
from chiralMS_settings import Ui_chiralMS_settings
from motor_control_settings import Ui_motor_control_settings
from open_hvc_controller import OpenHvcController


class chiral_ms_controller:
    def __init__(self) -> object:
        self.window_MS = QtWidgets.QMainWindow()
        self.ui_MS = Ui_chiralMS_settings()
        self.ui_MS.setupUi(self.window_MS)
        self.window_MS.show()

        # Standard hvc_settings file name
        self.filename = 'hvc_settings'

        # The motor control window
        def open_motor_control():  # TODO: Will require it's own controller
            self.window_MC = QtWidgets.QMainWindow()
            self.ui_MC = Ui_motor_control_settings()
            self.ui_MC.setupUi(self.window_MC)
            self.window_MC.show()

        # The high voltages control window
        def open_hvc():
            self.window_hvc = OpenHvcController()

        # The buttons for opening the hvc and motor control windows
        self.ui_MS.motor_control_button.clicked.connect(open_motor_control)
        self.ui_MS.voltage_control_button.clicked.connect(open_hvc)
