import main_gui_controller

from sys import argv
from PyQt5 import QtWidgets
from application import Ui_Application_name


class ApplicationController:
    def __init__(self):
        self.runner2 = None
        app = QtWidgets.QApplication(argv)
        self.application_window = QtWidgets.QMainWindow()
        self.ui_application = Ui_Application_name()
        self.ui_application.setupUi(self.application_window)
        self.application_window.show()
        self.ui_application.start_button.clicked.connect(self.start)
        exit(app.exec_())

    def start(self):
        self.runner2 = main_gui_controller.Controller()


if __name__ == '__main__':
    ApplicationController()
