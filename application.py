# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'application.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Application_name(object):
    def setupUi(self, Application_name):
        Application_name.setObjectName("Application_name")
        Application_name.resize(349, 81)
        self.centralwidget = QtWidgets.QWidget(Application_name)
        self.centralwidget.setObjectName("centralwidget")
        self.start_button = QtWidgets.QPushButton(self.centralwidget)
        self.start_button.setGeometry(QtCore.QRect(10, 20, 171, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        font.setBold(True)
        font.setWeight(75)
        self.start_button.setFont(font)
        self.start_button.setObjectName("start_button")
        Application_name.setCentralWidget(self.centralwidget)

        self.retranslateUi(Application_name)
        QtCore.QMetaObject.connectSlotsByName(Application_name)

    def retranslateUi(self, Application_name):
        _translate = QtCore.QCoreApplication.translate
        Application_name.setWindowTitle(_translate("Application_name", "Application_name"))
        self.start_button.setText(_translate("Application_name", "Start"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Application_name = QtWidgets.QMainWindow()
    ui = Ui_Application_name()
    ui.setupUi(Application_name)
    Application_name.show()
    sys.exit(app.exec_())
