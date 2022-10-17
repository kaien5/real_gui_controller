import json
import values as v
from os import getcwd
from PyQt5 import QtWidgets
from open_file_hvc import Ui_open_file_hvc
from save_file_as_hvc import Ui_save_window_hvc
from chiralMS_settings import Ui_chiralMS_settings
from high_voltage_control import Ui_high_voltage_control
from motor_control_settings import Ui_motor_control_settings


class chiral_ms_controller:
    def __init__(self) -> object:
        self.window_MS = QtWidgets.QMainWindow()
        self.ui_MS = Ui_chiralMS_settings()
        self.ui_MS.setupUi(self.window_MS)
        self.window_MS.show()

        # Standard hvc_settings file name
        self.filename = 'hvc_settings'

        # The motor control window
        def open_motor_control():
            self.window_MC = QtWidgets.QMainWindow()
            self.ui_MC = Ui_motor_control_settings()
            self.ui_MC.setupUi(self.window_MC)
            self.window_MC.show()

        # The high voltages control window
        def open_hvc():
            self.window_hvc = QtWidgets.QMainWindow()
            self.ui_hvc = Ui_high_voltage_control()
            self.ui_hvc.setupUi(self.window_hvc)
            self.window_hvc.show()

            def save_settings():
                hvc_settings = v.standard_hvc_settings
                hvc_settings["ip address"] = self.ui_hvc.ip_address_line.text()
                hvc_settings["connection name 1"] = self.ui_hvc.connections_line_1.text()
                hvc_settings["connection name 2"] = self.ui_hvc.connections_line_2.text()
                hvc_settings["connection name 3"] = self.ui_hvc.connections_line_3.text()
                hvc_settings["connection name 4"] = self.ui_hvc.connections_line_4.text()
                hvc_settings["connection name 5"] = self.ui_hvc.connections_line_5.text()
                hvc_settings["connection name 6"] = self.ui_hvc.connections_line_6.text()
                hvc_settings["module name 1"] = self.ui_hvc.model_information_name_line_1.text()
                hvc_settings["module name 2"] = self.ui_hvc.model_information_name_line_2.text()
                hvc_settings["module name 3"] = self.ui_hvc.model_information_name_line_3.text()
                hvc_settings["module name 4"] = self.ui_hvc.model_information_name_line_4.text()
                hvc_settings["module name 5"] = self.ui_hvc.model_information_name_line_5.text()
                hvc_settings["module name 6"] = self.ui_hvc.model_information_name_line_6.text()
                hvc_settings["min voltage 1"] = self.ui_hvc.model_information_min_line_1.text()
                hvc_settings["min voltage 2"] = self.ui_hvc.model_information_min_line_2.text()
                hvc_settings["min voltage 3"] = self.ui_hvc.model_information_min_line_3.text()
                hvc_settings["min voltage 4"] = self.ui_hvc.model_information_min_line_4.text()
                hvc_settings["min voltage 5"] = self.ui_hvc.model_information_min_line_5.text()
                hvc_settings["min voltage 6"] = self.ui_hvc.model_information_min_line_6.text()
                hvc_settings["max voltage 1"] = self.ui_hvc.model_information_max_line_1.text()
                hvc_settings["max voltage 2"] = self.ui_hvc.model_information_max_line_2.text()
                hvc_settings["max voltage 3"] = self.ui_hvc.model_information_max_line_3.text()
                hvc_settings["max voltage 4"] = self.ui_hvc.model_information_max_line_4.text()
                hvc_settings["max voltage 5"] = self.ui_hvc.model_information_max_line_5.text()
                hvc_settings["max voltage 6"] = self.ui_hvc.model_information_max_line_6.text()
                hvc_settings["voltage set 1"] = self.ui_hvc.new_setting_voltage_spinbox_1.value()
                hvc_settings["voltage set 2"] = self.ui_hvc.new_setting_voltage_spinbox_2.value()
                hvc_settings["voltage set 3"] = self.ui_hvc.new_setting_voltage_spinbox_3.value()
                hvc_settings["voltage set 4"] = self.ui_hvc.new_setting_voltage_spinbox_4.value()
                hvc_settings["voltage set 5"] = self.ui_hvc.new_setting_voltage_spinbox_5.value()
                hvc_settings["voltage set 6"] = self.ui_hvc.new_setting_voltage_spinbox_6.value()
                hvc_settings["delta V/s 1"] = self.ui_hvc.new_setting_delta_spinbox_1.value()
                hvc_settings["delta V/s 2"] = self.ui_hvc.new_setting_delta_spinbox_2.value()
                hvc_settings["delta V/s 3"] = self.ui_hvc.new_setting_delta_spinbox_3.value()
                hvc_settings["delta V/s 4"] = self.ui_hvc.new_setting_delta_spinbox_4.value()
                hvc_settings["delta V/s 5"] = self.ui_hvc.new_setting_delta_spinbox_5.value()
                hvc_settings["delta V/s 6"] = self.ui_hvc.new_setting_delta_spinbox_6.value()
                with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + self.filename + '.json', 'w') as f:
                    json.dump(hvc_settings, f)
                print(f'{self.filename} is saved at {getcwd()}\Chiral MS settings\High Voltage Control')

            def save_as_window():
                self.window_save = QtWidgets.QMainWindow()
                self.ui_save = Ui_save_window_hvc()
                self.ui_save.setupUi(self.window_save)
                self.window_save.show()

                def save_file_as():
                    self.filename = self.ui_save.save_as_hvc.text()
                    hvc_settings = v.standard_hvc_settings
                    hvc_settings["ip address"] = self.ui_hvc.ip_address_line.text()
                    hvc_settings["connection name 1"] = self.ui_hvc.connections_line_1.text()
                    hvc_settings["connection name 2"] = self.ui_hvc.connections_line_2.text()
                    hvc_settings["connection name 3"] = self.ui_hvc.connections_line_3.text()
                    hvc_settings["connection name 4"] = self.ui_hvc.connections_line_4.text()
                    hvc_settings["connection name 5"] = self.ui_hvc.connections_line_5.text()
                    hvc_settings["connection name 6"] = self.ui_hvc.connections_line_6.text()
                    hvc_settings["module name 1"] = self.ui_hvc.model_information_name_line_1.text()
                    hvc_settings["module name 2"] = self.ui_hvc.model_information_name_line_2.text()
                    hvc_settings["module name 3"] = self.ui_hvc.model_information_name_line_3.text()
                    hvc_settings["module name 4"] = self.ui_hvc.model_information_name_line_4.text()
                    hvc_settings["module name 5"] = self.ui_hvc.model_information_name_line_5.text()
                    hvc_settings["module name 6"] = self.ui_hvc.model_information_name_line_6.text()
                    hvc_settings["min voltage 1"] = self.ui_hvc.model_information_min_line_1.text()
                    hvc_settings["min voltage 2"] = self.ui_hvc.model_information_min_line_2.text()
                    hvc_settings["min voltage 3"] = self.ui_hvc.model_information_min_line_3.text()
                    hvc_settings["min voltage 4"] = self.ui_hvc.model_information_min_line_4.text()
                    hvc_settings["min voltage 5"] = self.ui_hvc.model_information_min_line_5.text()
                    hvc_settings["min voltage 6"] = self.ui_hvc.model_information_min_line_6.text()
                    hvc_settings["max voltage 1"] = self.ui_hvc.model_information_max_line_1.text()
                    hvc_settings["max voltage 2"] = self.ui_hvc.model_information_max_line_2.text()
                    hvc_settings["max voltage 3"] = self.ui_hvc.model_information_max_line_3.text()
                    hvc_settings["max voltage 4"] = self.ui_hvc.model_information_max_line_4.text()
                    hvc_settings["max voltage 5"] = self.ui_hvc.model_information_max_line_5.text()
                    hvc_settings["max voltage 6"] = self.ui_hvc.model_information_max_line_6.text()
                    hvc_settings["voltage set 1"] = self.ui_hvc.new_setting_voltage_spinbox_1.value()
                    hvc_settings["voltage set 2"] = self.ui_hvc.new_setting_voltage_spinbox_2.value()
                    hvc_settings["voltage set 3"] = self.ui_hvc.new_setting_voltage_spinbox_3.value()
                    hvc_settings["voltage set 4"] = self.ui_hvc.new_setting_voltage_spinbox_4.value()
                    hvc_settings["voltage set 5"] = self.ui_hvc.new_setting_voltage_spinbox_5.value()
                    hvc_settings["voltage set 6"] = self.ui_hvc.new_setting_voltage_spinbox_6.value()
                    hvc_settings["delta V/s 1"] = self.ui_hvc.new_setting_delta_spinbox_1.value()
                    hvc_settings["delta V/s 2"] = self.ui_hvc.new_setting_delta_spinbox_2.value()
                    hvc_settings["delta V/s 3"] = self.ui_hvc.new_setting_delta_spinbox_3.value()
                    hvc_settings["delta V/s 4"] = self.ui_hvc.new_setting_delta_spinbox_4.value()
                    hvc_settings["delta V/s 5"] = self.ui_hvc.new_setting_delta_spinbox_5.value()
                    hvc_settings["delta V/s 6"] = self.ui_hvc.new_setting_delta_spinbox_6.value()
                    with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + self.filename + '.json', 'w') as f:
                        json.dump(hvc_settings, f)
                    self.window_save.close()
                    print(f'{self.filename} is saved at {getcwd()}\Chiral MS settings\High Voltage Control')

                # The ok / cancel button functions
                self.ui_save.save_file_as_hvc.accepted.connect(save_file_as)
                self.ui_save.save_file_as_hvc.rejected.connect(self.window_save.close)

            def open_window():
                self.window_open = QtWidgets.QMainWindow()
                self.ui_open = Ui_open_file_hvc()
                self.ui_open.setupUi(self.window_open)
                self.window_open.show()

                def open_hvc_file():
                    self.filename = self.ui_open.open_hvc.text()
                    try:
                        with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + self.filename + '.json',
                                  'r') as f:
                            hvc_settings = json.load(f)
                            self.ui_hvc.ip_address_line.setText(hvc_settings["ip address"])
                            self.ui_hvc.connections_line_1.setText(hvc_settings["connection name 1"])
                            self.ui_hvc.connections_line_2.setText(hvc_settings["connection name 2"])
                            self.ui_hvc.connections_line_3.setText(hvc_settings["connection name 3"])
                            self.ui_hvc.connections_line_4.setText(hvc_settings["connection name 4"])
                            self.ui_hvc.connections_line_5.setText(hvc_settings["connection name 5"])
                            self.ui_hvc.connections_line_6.setText(hvc_settings["connection name 6"])
                            self.ui_hvc.model_information_name_line_1.setText(hvc_settings["module name 1"])
                            self.ui_hvc.model_information_name_line_2.setText(hvc_settings["module name 2"])
                            self.ui_hvc.model_information_name_line_3.setText(hvc_settings["module name 3"])
                            self.ui_hvc.model_information_name_line_4.setText(hvc_settings["module name 4"])
                            self.ui_hvc.model_information_name_line_5.setText(hvc_settings["module name 5"])
                            self.ui_hvc.model_information_name_line_6.setText(hvc_settings["module name 6"])
                            self.ui_hvc.model_information_min_line_1.setText(hvc_settings["min voltage 1"])
                            self.ui_hvc.model_information_min_line_2.setText(hvc_settings["min voltage 2"])
                            self.ui_hvc.model_information_min_line_3.setText(hvc_settings["min voltage 3"])
                            self.ui_hvc.model_information_min_line_4.setText(hvc_settings["min voltage 4"])
                            self.ui_hvc.model_information_min_line_5.setText(hvc_settings["min voltage 5"])
                            self.ui_hvc.model_information_min_line_6.setText(hvc_settings["min voltage 6"])
                            self.ui_hvc.model_information_max_line_1.setText(hvc_settings["max voltage 1"])
                            self.ui_hvc.model_information_max_line_2.setText(hvc_settings["max voltage 2"])
                            self.ui_hvc.model_information_max_line_3.setText(hvc_settings["max voltage 3"])
                            self.ui_hvc.model_information_max_line_4.setText(hvc_settings["max voltage 4"])
                            self.ui_hvc.model_information_max_line_5.setText(hvc_settings["max voltage 5"])
                            self.ui_hvc.model_information_max_line_6.setText(hvc_settings["max voltage 6"])
                            self.ui_hvc.new_setting_voltage_spinbox_1.setValue(hvc_settings["voltage set 1"])
                            self.ui_hvc.new_setting_voltage_spinbox_2.setValue(hvc_settings["voltage set 2"])
                            self.ui_hvc.new_setting_voltage_spinbox_3.setValue(hvc_settings["voltage set 3"])
                            self.ui_hvc.new_setting_voltage_spinbox_4.setValue(hvc_settings["voltage set 4"])
                            self.ui_hvc.new_setting_voltage_spinbox_5.setValue(hvc_settings["voltage set 5"])
                            self.ui_hvc.new_setting_voltage_spinbox_6.setValue(hvc_settings["voltage set 6"])
                            self.ui_hvc.new_setting_delta_spinbox_1.setValue(hvc_settings["delta V/s 1"])
                            self.ui_hvc.new_setting_delta_spinbox_2.setValue(hvc_settings["delta V/s 2"])
                            self.ui_hvc.new_setting_delta_spinbox_3.setValue(hvc_settings["delta V/s 3"])
                            self.ui_hvc.new_setting_delta_spinbox_4.setValue(hvc_settings["delta V/s 4"])
                            self.ui_hvc.new_setting_delta_spinbox_5.setValue(hvc_settings["delta V/s 5"])
                            self.ui_hvc.new_setting_delta_spinbox_6.setValue(hvc_settings["delta V/s 6"])
                            self.window_open.close()
                    except FileNotFoundError:
                        print('File is not in the directory')

                # The ok / cancel button functions
                self.ui_open.open_file.accepted.connect(open_hvc_file)
                self.ui_open.open_file.rejected.connect(self.window_open.close)

            # The drop-down menu and their functions
            self.ui_hvc.actionSave.triggered.connect(save_settings)
            self.ui_hvc.actionSave_as.triggered.connect(save_as_window)
            self.ui_hvc.actionOpen.triggered.connect(open_window)

            # Exit button will connect to close_window function
            self.ui_hvc.exit_button.clicked.connect(self.window_hvc.close)

        # The buttons for opening the hvc and motor control windows
        self.ui_MS.motor_control_button.clicked.connect(open_motor_control)
        self.ui_MS.voltage_control_button.clicked.connect(open_hvc)
