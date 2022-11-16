import struct

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QTableWidgetItem
from pymodbus.client.sync import ModbusTcpClient
from microGC import Ui_microGC_settings

import values as v
import file_browser


class MicroGcController:
    def __init__(self, file=False, data=None):
        self.fileBrowserWidget = None
        self.window_GC = QtWidgets.QMainWindow()
        self.ui_GC = Ui_microGC_settings()
        self.ui_GC.setupUi(self.window_GC)
        self.window_GC.show()

        # The settings for the plot
        self.ui_GC.temperature_trajectory.canvas.fig.text(0.82, 0.16, '(min)', ha='center', va='center')
        self.ui_GC.temperature_trajectory.canvas.fig.text(0.02, 0.5, 'Temperature (°C)', ha='center', va='center', rotation='vertical')
        self.ui_GC.temperature_trajectory.canvas.ax.grid()

        # The buttons and their function
        self.ui_GC.set_graph.clicked.connect(self.update_graph)
        self.ui_GC.refresh_button.clicked.connect(self.refresh)
        self.ui_GC.remove_row.clicked.connect(self.remove_row)
        self.ui_GC.add_row.clicked.connect(self.add_row)

        # The Drop-down menu and their functions
        self.ui_GC.action_Save.triggered.connect(self.save_file_browser)
        self.ui_GC.action_Open.triggered.connect(self.open_file_browser)

        # Checking if settings are supplied, else use the standard settings
        if file:
            microGC_settings = data
        else:
            microGC_settings = v.standard_microGC_settings

        self.ui_GC.column_oven_temp.setText(microGC_settings["Column temperature"])
        self.ui_GC.column_pressure.setText(microGC_settings["Column carrier pressure"])
        self.ui_GC.injection_temp.setText(microGC_settings["Injection temperature"])
        self.ui_GC.method_name.setText(microGC_settings["Method name"])
        self.ui_GC.heated_sample_line_temp.setText(microGC_settings["Heated sample line temp"])
        self.ui_GC.injection_time.setText(microGC_settings["Injection time"])
        self.ui_GC.analysis_time.setText(microGC_settings["Analysis time"])
        self.ui_GC.backflush_time.setText(microGC_settings["Back-flush time"])
        self.ui_GC.cycle_time.setText(microGC_settings["Cycle time"])
        self.ui_GC.number_of_analysis.setText(microGC_settings["# of analysis per sequence"])

        # Equalizing the table row count to size of "Rate"
        while self.ui_GC.temperature_table.rowCount() < len(microGC_settings["Rate"]):
            self.ui_GC.temperature_table.insertRow(self.ui_GC.temperature_table.rowCount())

        # Equalizing the table row count to size of "Rate"
        while self.ui_GC.temperature_table.rowCount() > len(microGC_settings["Rate"]):
            self.ui_GC.temperature_table.removeRow(self.ui_GC.temperature_table.rowCount() - 1)

        # Filling in the table
        for i in range(len(microGC_settings["Rate"])):
            self.ui_GC.temperature_table.setItem(i, 0, QTableWidgetItem(microGC_settings["Rate"][i]))
            self.ui_GC.temperature_table.setItem(i, 1, QTableWidgetItem(microGC_settings["Final temp"][i]))
            self.ui_GC.temperature_table.setItem(i, 2, QTableWidgetItem(microGC_settings["Hold time"][i]))

    def refresh(self):
        try:
            microGC_ip = self.ui_GC.ip_address.text()
            self.client = ModbusTcpClient(host=microGC_ip, port='502')
            self.client.connect()

            test = [30900, 30916, 30908, 30700]  # 30700 might be wrong
            data = {}
            for i in test:
                register = self.client.read_input_registers(i, 2)
                raw = struct.pack('>HH', register.registers[0], register.registers[1])
                data['Register ' + str(i)] = str(struct.unpack('>f', raw)[0])

            self.ui_GC.column_oven_temp.setText(str(data['Register 30900']))
            self.ui_GC.column_pressure.setText(str(data['Register 30916']))
            self.ui_GC.injection_temp.setText(str(data['Register 30908']))
            self.ui_GC.heated_sample_line_temp.setText(str(data['Register 30700']))

            self.client.close()

        except Exception as e:
            print(e)

    # Opening the save file browser and supplying the settings
    def save_file_browser(self):
        # Empty lists for the columns in the table
        rate = []
        final_temp = []
        hold_time = []

        # Collecting the data from the table
        try:
            for i in range(self.ui_GC.temperature_table.rowCount()):
                rate.append(self.ui_GC.temperature_table.item(i, 0).text())
                final_temp.append(self.ui_GC.temperature_table.item(i, 1).text())
                hold_time.append((self.ui_GC.temperature_table.item(i, 2).text()))

            # The microGC settings
            microGC_settings = v.standard_microGC_settings
            microGC_settings["Column temperature"] = self.ui_GC.column_oven_temp.text()
            microGC_settings["Column carrier pressure"] = self.ui_GC.column_pressure.text()
            microGC_settings["Injection temperature"] = self.ui_GC.injection_temp.text()
            microGC_settings["Method name"] = self.ui_GC.method_name.text()
            microGC_settings["Heated sample line temp"] = self.ui_GC.heated_sample_line_temp.text()
            microGC_settings["Injection time"] = self.ui_GC.injection_time.text()
            microGC_settings["Analysis time"] = self.ui_GC.analysis_time.text()
            microGC_settings["Back-flush time"] = self.ui_GC.backflush_time.text()
            microGC_settings["Cycle time"] = self.ui_GC.cycle_time.text()
            microGC_settings["# of analysis per sequence"] = self.ui_GC.number_of_analysis.text()
            microGC_settings["Rate"] = rate
            microGC_settings["Final temp"] = final_temp
            microGC_settings["Hold time"] = hold_time

            # Opening the filebrowser with the settings supplied
            self.fileBrowserWidget = file_browser.FileBrowserController(save_file=True, microGC=True, microGC_data=microGC_settings)
            self.fileBrowserWidget.show()
            self.fileBrowserWidget.set_path()

        except Exception as e:
            print(f'All fields must contain data. Error: {e}')

    # Opening the file browser
    def open_file_browser(self):
        self.window_GC.close()
        self.fileBrowserWidget = file_browser.FileBrowserController(open_file=True, microGC=True)
        self.fileBrowserWidget.show()
        self.fileBrowserWidget.set_path()

    # Updating the graph
    def update_graph(self):
        try:
            # Clear the previous data
            self.ui_GC.temperature_trajectory.canvas.ax.clear()
            self.ui_GC.temperature_trajectory.canvas.ax.grid()

            # The initial temperature and time
            temperature_trajectory = [float(self.ui_GC.temperature_table.item(0, 1).text())]
            time_trajectory = [0]

            # The plot data for the range of the table
            for i in range(1, self.ui_GC.temperature_table.rowCount()):
                temperature_trajectory.append(float(self.ui_GC.temperature_table.item(i, 1).text()))
                time_end = time_trajectory[-1] + (abs(temperature_trajectory[-1] - temperature_trajectory[-2]) /
                                                  float(self.ui_GC.temperature_table.item(i, 0).text()))
                time_trajectory.append(time_end)

                # When hold time is > 0 then append another data point
                if float(self.ui_GC.temperature_table.item(i, 2).text()) > 0:
                    temperature_trajectory.append(float(self.ui_GC.temperature_table.item(i, 1).text()))
                    time_trajectory.append(time_trajectory[-1] + float(self.ui_GC.temperature_table.item(i, 2).text()))

            # Plot the data
            self.ui_GC.temperature_trajectory.canvas.ax.plot(time_trajectory, temperature_trajectory)
            self.ui_GC.temperature_trajectory.canvas.draw()

            # Updating the total time label
            self.ui_GC.total_time.setText(str(round(time_trajectory[-1], 2)))

        except Exception as e:
            print(f'All fields must contain data. Error: {e}')

    # Adds a row in the table
    def add_row(self):
        self.ui_GC.temperature_table.insertRow(self.ui_GC.temperature_table.rowCount())

    # Removes a row in the table
    def remove_row(self):
        self.ui_GC.temperature_table.removeRow(self.ui_GC.temperature_table.rowCount() - 1)
