from PyQt5 import QtWidgets
from injector import Ui_injector_settings


class Injector_controller:
    def __init__(self):
        self.window_in = QtWidgets.QMainWindow()
        self.ui_in = Ui_injector_settings()
        self.ui_in.setupUi(self.window_in)
        self.window_in.show()
