from PyQt5 import QtWidgets, QtCore
from warning_window import Ui_warning_window


class WarningWindow:
    def __init__(self, text='test'):
        self.warning_window = QtWidgets.QMainWindow()
        self.ui_warning = Ui_warning_window()
        self.ui_warning.setupUi(self.warning_window)

        # The text of the warning
        self.text = str(text)

        # Set the text of the warning
        self.ui_warning.warning_label.setText(self.text)
        self.ui_warning.warning_label.adjustSize()
        text_width = self.ui_warning.warning_label.size().width()

        self.warning_window.setFixedWidth(text_width + 20)
        self.warning_window.setFixedHeight(80)

        window_width = self.warning_window.width()
        self.ui_warning.ok_button.setGeometry(QtCore.QRect(round(window_width / 2 - 23), 50, 75, 23))

        self.warning_window.show()

        # The buttons and their functions
        self.ui_warning.ok_button.clicked.connect(self.close_window)

    def close_window(self):
        self.warning_window.close()
