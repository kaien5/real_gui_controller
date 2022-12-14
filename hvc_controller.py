import values as v
import file_browser

from PyQt5 import QtWidgets
from hvc import Ui_high_voltage_control


class HvcController:
    def __init__(self, file=False, data=None):
        self.fileBrowserWidget = None
        self.window_hvc = QtWidgets.QMainWindow()
        self.ui_hvc = Ui_high_voltage_control()
        self.ui_hvc.setupUi(self.window_hvc)
        self.window_hvc.show()

        # The drop-down menu and their functions
        self.ui_hvc.actionOpen.triggered.connect(self.open_file)
        self.ui_hvc.actionSave.triggered.connect(self.save_file)

        if file:
            hvc_settings = data
        else:
            hvc_settings = v.standard_hvc_settings

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

    # Opening the file browser
    def open_file(self):
        self.window_hvc.close()
        self.fileBrowserWidget = file_browser.FileBrowserController(open_file=True, hvc=True)
        self.fileBrowserWidget.show()
        self.fileBrowserWidget.set_path()

    # Saving settings and supplying this to the filebrowser
    def save_file(self):
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

        self.fileBrowserWidget = file_browser.FileBrowserController(save_file=True, hvc=True, hvc_data=hvc_settings)
        self.fileBrowserWidget.show()
        self.fileBrowserWidget.set_path()
