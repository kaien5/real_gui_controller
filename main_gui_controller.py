import socket
import h5py
import struct
import numpy as np
import values as v
import file_browser
import dynamiq_import
import tof_ms_analysis as tof

from time import sleep
from PyQt5 import QtWidgets
from main_gui import Ui_MainWindow
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from microGC_controller import MicroGcController
from pymodbus.payload import BinaryPayloadDecoder
from warning_window_controller import WarningWindow
from PyQt5.QtCore import QObject, pyqtSignal, QThread
from labview_communication import ascii_message, pack_payload
from electron_image_controller import ElectronImageController


check = True


class Controller:
    def __init__(self, load=False, data=None):
        self.ix = None
        self.x1 = None
        self.x2 = None
        self.y1 = None
        self.y2 = None
        self.wait = None
        self.ui_EC = None
        self.client = None
        self.loaded = False
        self.worker1 = None
        self.thread1 = None
        self.brackets = None
        self.filename = None
        self.window_in = None
        self.window_GC = None
        self.window_hvc = None
        self.first_click = True
        self.window_motor = None
        self.compound_data = None
        self.labview_client = None
        self.compound_names = None
        self.warning_window = None
        self.sequence_names = None
        self.fileBrowserWidget = None
        self.labview_client_message = None

        # The MainWindow setup
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        # Maximizing the screen
        self.MainWindow.showMaximized()

        # The buttons and their functions
        self.ui.microGC_settings_button.clicked.connect(self.open_micro_gc_window)
        self.ui.disconnect_button_labview.clicked.connect(self.disconnect_labview)
        self.ui.send_button_labview.clicked.connect(self.send_message_labview)
        self.ui.connect_button_micro_GC.clicked.connect(self.connect_micro_GC)
        self.ui.sequence_number.valueChanged.connect(self.sequence_selection)
        self.ui.connect_button_labview.clicked.connect(self.connect_labview)
        self.ui.reset_chromatogram.clicked.connect(self.reset_chromatograms)
        self.ui.chromatogram_table.clicked.connect(self.table_click)
        self.ui.action_Open.triggered.connect(self.open_file)
        self.ui.load_button.clicked.connect(self.load_data)
        self.ui.start_button.clicked.connect(self.start)
        self.ui.enable_plots.toggled.connect(self.plots)
        self.ui.stop_button.clicked.connect(self.stop)
        self.ui.zoom_box.clicked.connect(self.zoom)
        self.ui.line_box.clicked.connect(self.line)

        # Clicked on functions
        self.ui.Ch1_FF.canvas.mpl_connect('button_press_event', self.plot_click), self.ui.Ch1_FF.canvas.mpl_connect('button_release_event', self.plot_click)
        self.ui.Ch2_FF.canvas.mpl_connect('button_press_event', self.plot_click), self.ui.Ch2_FF.canvas.mpl_connect('button_release_event', self.plot_click)
        self.ui.Ch2_BF.canvas.mpl_connect('button_press_event', self.plot_click), self.ui.Ch2_BF.canvas.mpl_connect('button_release_event', self.plot_click)
        self.ui.electron_image.canvas.mpl_connect('button_press_event', self.electron_image_click)

        # Disabling the plots at start up
        self.ui.Ch1_FF.setEnabled(False)
        self.ui.Ch2_FF.setEnabled(False)
        self.ui.Ch2_BF.setEnabled(False)
        self.ui.mass_spectrum.setEnabled(False)
        self.ui.electron_image.setEnabled(False)

        # Hiding the axis from the electron image
        self.ui.electron_image.canvas.ax.axis('off')

        # Load data from supplied file
        if load:
            self.ui.enable_plots.setEnabled(True)

            self.time, self.Ch1_FF, self.Ch2_FF, self.Ch2_BF = data[0], data[1], data[2], data[3]
            self.Ch1_FF_x1 = self.Ch2_FF_x1 = self.Ch2_BF_x1 = min(self.time) - max(self.time) * 0.05
            self.Ch1_FF_x2 = self.Ch2_FF_x2 = self.Ch2_BF_x2 = max(self.time) + max(self.time) * 0.05
            self.Ch1_FF_y1, self.Ch1_FF_y2 = min(self.Ch1_FF) - max(self.Ch1_FF) * 0.05, max(self.Ch1_FF) + max(self.Ch1_FF) * 0.05
            self.Ch2_FF_y1, self.Ch2_FF_y2 = min(self.Ch2_FF) - max(self.Ch2_FF) * 0.05, max(self.Ch2_FF) + max(self.Ch2_FF) * 0.05
            self.Ch2_BF_y1, self.Ch2_BF_y2 = min(self.Ch2_BF) - max(self.Ch2_BF) * 0.05, max(self.Ch2_BF) + max(self.Ch2_BF) * 0.05

    # Connect to the LabView script and send a start message
    def connect_labview(self):
        try:
            # Connecting to the TCP listen (Labview)
            self.labview_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.labview_client.connect(('localhost', 6340))

            # Sending message 'start'
            self.labview_client.sendall('START'.encode('utf-8'))
            self.labview_client.close()

            self.ui.disconnect_button_labview.setEnabled(True)
            self.ui.connect_button_labview.setEnabled(False)
            self.ui.send_button_labview.setEnabled(True)

        except Exception as e:
            self.warning_window = WarningWindow(text=e)

    # Disconnect from the LabView script and send
    def disconnect_labview(self):
        try:
            # Connecting to the TCP listen (Labview)
            self.labview_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.labview_client.connect(('localhost', 6340))

            # Sending message 'stop'
            self.labview_client.sendall('STOP'.encode('utf-8'))
            self.labview_client.close()

            self.ui.disconnect_button_labview.setEnabled(False)
            self.ui.connect_button_labview.setEnabled(True)
            self.ui.send_button_labview.setEnabled(False)

        except Exception as e:
            self.warning_window = WarningWindow(text=e)

    # Send a message to the LabView script when connected
    def send_message_labview(self):
        try:
            self.labview_client_message = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.labview_client_message.connect(('localhost', 6340))

            indicator_message = ascii_message(self.ui.indicator_line.text())
            command_message = ascii_message(self.ui.command_line.text())
            payload_message = pack_payload(self.ui.payload_double.value())
            message = indicator_message + command_message + payload_message

            self.labview_client_message.sendall(message)
            self.labview_client_message.close()

            if self.ui.command_line.text() == 'STOP':
                self.disconnect_labview()

        except Exception as e:
            self.warning_window = WarningWindow(text=e)

    # The function to start the data acquisition
    def start(self):
        global check
        try:
            microGC_ip = self.ui.ip_address_microGC.text()
            self.client = ModbusTcpClient(host=microGC_ip, port='502')
            self.client.connect()

            # This function will select the sequence to run and start as well
            self.client.write_register(0x9D0A, 0x0001)  # Stop all queued sequences
            self.client.write_register(0x9C41, self.ui.sequence_number.value())
            self.client.write_register(0x9D08, 0x0001)
            self.ui.connect_button_micro_GC.setEnabled(False)
            self.ui.start_button.setEnabled(False)
            self.ui.load_button.setEnabled(False)

            self.wait = True
            check = True

            self.thread1 = QThread()
            self.worker1 = Worker1()
            self.worker1.moveToThread(self.thread1)
            self.thread1.started.connect(self.worker1.run)
            self.worker1.finished1.connect(self.thread1.quit)
            self.worker1.finished1.connect(self.worker1.deleteLater)
            self.thread1.finished.connect(self.thread1.deleteLater)
            self.worker1.progress1.connect(self.check_microGC)
            self.thread1.start()

        except Exception as e:
            self.ui.microGC_status.setText('Invalid IP Address')
            self.warning_window = WarningWindow(text=e)

    # The function to stop data acquisition
    def stop(self):
        global check
        try:
            self.client.write_register(0x9D0A, 1)
            self.client.close()
            self.ui.connect_button_micro_GC.setEnabled(True)
            self.ui.start_button.setEnabled(True)
            self.ui.stop_button.setEnabled(False)
            check = False
            self.ui.microGC_status.setText('Run cancelled')

        except Exception as e:
            self.warning_window = WarningWindow(text=e)

    # The function to open a file
    def open_file(self):
        self.MainWindow.close()
        self.fileBrowserWidget = file_browser.FileBrowserController(open_file=True, main=True)
        self.fileBrowserWidget.show()
        self.fileBrowserWidget.set_path()

    # The function to check the connection of the machines
    def connect_micro_GC(self):
        try:
            microGC_ip = self.ui.ip_address_microGC.text()
            self.client = ModbusTcpClient(host=microGC_ip, port='502')
            self.client.connect()

            self.ui.microGC_status.setText('Connected')

            number_of_sequences = self.client.read_input_registers(31401, 1).registers[0]  # The number of sequences on instrument
            self.ui.sequence_number.setMaximum(number_of_sequences)  # Setting the sequence number value to the amount of sequences

            self.sequence_names = {}
            for i in range(number_of_sequences):
                register = self.client.read_input_registers(31602 + (i * 10), 20)
                decoder = BinaryPayloadDecoder.fromRegisters(register.registers, byteorder=Endian.Big, wordorder=Endian.Big)
                self.sequence_names['Sequence ' + str(i + 1)] = decoder.decode_string(20).decode().replace('\x00', '')

            self.client.close()
            self.ui.sequence_number.setValue(4)
            self.ui.sequence_label.setText(self.sequence_names['Sequence ' + str(self.ui.sequence_number.value())])

            # Enabling some buttons
            self.ui.microGC_settings_button.setEnabled(True)
            self.ui.sequence_number.setEnabled(True)
            self.ui.start_button.setEnabled(True)
            self.ui.load_button.setEnabled(True)

        except Exception as e:
            self.ui.microGC_status.setText('Unable to connect')
            self.warning_window = WarningWindow(text=e)

    # This function is to check whether the MicroGC is busy
    def check_microGC(self):
        global check

        if self.wait:
            self.ui.microGC_status.setText('Waiting for response...')
            response = self.client.read_discrete_inputs(0x2712, 1)
            if response.bits[0]:
                self.wait = False

        else:
            response = self.client.read_discrete_inputs(0x2712, 1)
            progress = self.client.read_input_registers(30542, 1)
            if response.bits[0]:
                self.ui.microGC_status.setText(f'Running {progress.registers[0]}%')
                self.ui.stop_button.setEnabled(True)
            else:
                self.ui.microGC_status.setText('Done')
                self.ui.connect_button_micro_GC.setEnabled(True)
                self.ui.stop_button.setEnabled(False)
                self.ui.start_button.setEnabled(True)
                self.ui.load_button.setEnabled(True)
                check = False
            self.client.close()

    # The function to select a sequence on the microGC
    def sequence_selection(self):
        self.ui.sequence_label.setText(self.sequence_names['Sequence ' + str(self.ui.sequence_number.value())])

    # The function to load in data from the connected machines
    def load_data(self):
        # Communicating to the plot function
        self.loaded = True

        # Enabling the plots and the plot enable button
        self.ui.enable_plots.setEnabled(True)
        self.ui.mass_spectrum.setEnabled(False)
        self.ui.electron_image.setEnabled(False)

        # Connect to the IP written in the text line
        microGC_ip = self.ui.ip_address_microGC.text()

        try:
            self.filename = dynamiq_import.load(host=microGC_ip, port=7197)

        except Exception as e:
            self.warning_window = WarningWindow(text=e)

        # Importing the method name
        register = self.client.read_input_registers(32000, 10)
        decoder = BinaryPayloadDecoder.fromRegisters(register.registers, byteorder=Endian.Big, wordorder=Endian.Big)
        last_method = str(decoder.decode_string(20).decode()).replace('\x00', '')
        self.ui.last_method.setText(last_method)

        # The number of compounds found in the last run
        self.compound_data = {}
        number_of_compounds = self.client.read_input_registers(35000, 1).registers[0]

        # Extracting the compound data from the DynamicQ
        for i in range(number_of_compounds):
            register = self.client.read_input_registers(35001 + i * 10, 10)
            decoder = BinaryPayloadDecoder.fromRegisters(register.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            compounds = decoder.decode_string(20).decode().replace('\x00', '')

            # The contents for the table
            values = []
            for _ in range(7):
                register = self.client.read_input_registers(35401 + i * 2 + _ * 80, 2)
                concentration = str(round(struct.unpack('>f', struct.pack('>HH', register.registers[0], register.registers[1]))[0], 2))
                values.append(concentration)

            for _ in range(2):
                channel_number = self.client.read_input_registers(36121 + i + _ * 40, 1).registers[0]
                values.append(str(channel_number))

            self.compound_data[compounds] = values

        # Loading the compound names
        self.compound_names = []
        for index, key in enumerate(self.compound_data):
            self.compound_names.append(key)

        # The horizontal headers
        for i in range(len(v.column_names)):
            if self.ui.chromatogram_table.columnCount() < len(v.column_names):
                self.ui.chromatogram_table.insertColumn(i)
                self.ui.chromatogram_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(v.column_names[i]))

        # The vertical headers
        for i in range(number_of_compounds):
            if self.ui.chromatogram_table.rowCount() < number_of_compounds:
                self.ui.chromatogram_table.insertRow(i)
            self.ui.chromatogram_table.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(self.compound_names[i]))

        # The table contents
        for i in range(number_of_compounds):
            for _ in range(len(v.column_names)):
                if _ == 8:
                    if int(self.compound_data[self.compound_names[i]][_]) == 1:
                        self.ui.chromatogram_table.setItem(i, _, QtWidgets.QTableWidgetItem('FF'))
                    elif int(self.compound_data[self.compound_names[i]][_]) == 2:
                        self.ui.chromatogram_table.setItem(i, _, QtWidgets.QTableWidgetItem('BF'))

                else:
                    self.ui.chromatogram_table.setItem(i, _, QtWidgets.QTableWidgetItem(self.compound_data[self.compound_names[i]][_]))

                # Centering the horizontal text alignment
                self.ui.chromatogram_table.item(i, _).setTextAlignment(0x0004)

        # Resizing the columns and rows to their contents
        self.ui.chromatogram_table.resizeColumnsToContents()
        self.ui.chromatogram_table.resizeRowsToContents()

        # The brackets for the compounds in the plots
        self.brackets = {}
        for i in range(len(self.compound_names)):
            if float(self.compound_data[self.compound_names[i]][5]) > 0:
                x1 = [float(self.compound_data[self.compound_names[i]][5]), float(self.compound_data[self.compound_names[i]][5])]
                x2 = [float(self.compound_data[self.compound_names[i]][6]), float(self.compound_data[self.compound_names[i]][6])]
                y = [-5, 100]
                begin = x1, y
                end = x2, y
                self.brackets[self.compound_names[i]] = begin, end

        # The data for the plots
        self.time = np.loadtxt(str(self.filename), skiprows=3, usecols=0)
        self.Ch1_FF = np.loadtxt(str(self.filename), skiprows=3, usecols=1)
        self.Ch2_FF = np.loadtxt(str(self.filename), skiprows=3, usecols=2)
        self.Ch2_BF = np.loadtxt(str(self.filename), skiprows=3, usecols=3)

        # The values for the x and y limit
        self.Ch1_FF_x1 = self.Ch2_FF_x1 = self.Ch2_BF_x1 = min(self.time) - max(self.time) * 0.05
        self.Ch1_FF_x2 = self.Ch2_FF_x2 = self.Ch2_BF_x2 = max(self.time) + max(self.time) * 0.05
        self.Ch1_FF_y1, self.Ch1_FF_y2 = min(self.Ch1_FF) - max(self.Ch1_FF) * 0.05, max(self.Ch1_FF) + max(self.Ch1_FF) * 0.05
        self.Ch2_FF_y1, self.Ch2_FF_y2 = min(self.Ch2_FF) - max(self.Ch2_FF) * 0.05, max(self.Ch2_FF) + max(self.Ch2_FF) * 0.05
        self.Ch2_BF_y1, self.Ch2_BF_y2 = min(self.Ch2_BF) - max(self.Ch2_BF) * 0.05, max(self.Ch2_BF) + max(self.Ch2_BF) * 0.05

        # Refreshing the plots
        if self.ui.enable_plots.isChecked():
            self.ui.enable_plots.toggle()
            self.ui.enable_plots.toggle()
        else:
            self.ui.enable_plots.toggle()

        # Closing the connection to the client
        self.client.close()

    # The function to enable or disable the plots
    def plots(self, draw=True):
        if self.ui.enable_plots.checkState():
            self.ui.Ch1_FF.setEnabled(True), self.ui.Ch2_FF.setEnabled(True), self.ui.Ch2_BF.setEnabled(True)

            # Clearing the plots
            self.ui.Ch1_FF.canvas.ax.clear(), self.ui.Ch1_FF.canvas.fig.texts.clear()
            self.ui.Ch2_FF.canvas.ax.clear(), self.ui.Ch2_FF.canvas.fig.texts.clear()
            self.ui.Ch2_BF.canvas.ax.clear(), self.ui.Ch2_BF.canvas.fig.texts.clear()
            self.ui.mass_spectrum.canvas.ax.clear(), self.ui.electron_image.canvas.ax.clear()

            # Hiding the axis from the electron image
            self.ui.electron_image.canvas.ax.axis('off')

            # Labeling the axes
            self.ui.Ch1_FF.canvas.ax.set_xlabel('Retention time (min)'), self.ui.Ch1_FF.canvas.ax.set_ylabel('Intensity')
            self.ui.Ch2_FF.canvas.ax.set_xlabel('Retention time (min)'), self.ui.Ch2_FF.canvas.ax.set_ylabel('Intensity')
            self.ui.Ch2_BF.canvas.ax.set_xlabel('Retention time (min)'), self.ui.Ch2_BF.canvas.ax.set_ylabel('Intensity')

            # Enabling the grid
            self.ui.Ch1_FF.canvas.ax.grid(True, 'both'), self.ui.Ch2_FF.canvas.ax.grid(True, 'both'), self.ui.Ch2_BF.canvas.ax.grid(True, 'both')

            # Showing the titles of the plots
            self.ui.Ch1_FF.canvas.ax.set_title('Ch1 (FF)')
            self.ui.Ch2_FF.canvas.ax.set_title('Ch2 (FF)')
            self.ui.Ch2_BF.canvas.ax.set_title('Ch2 (BF)')
            self.ui.mass_spectrum.canvas.ax.set_title('Mass spectrum')
            self.ui.electron_image.canvas.ax.set_title('Electron image')

            # Plotting the data and brackets
            self.ui.Ch1_FF.canvas.ax.plot(self.time, self.Ch1_FF, 'b')
            self.ui.Ch2_FF.canvas.ax.plot(self.time, self.Ch2_FF, 'b')
            self.ui.Ch2_BF.canvas.ax.plot(self.time, self.Ch2_BF, 'b')

            # Enabling the chromatogram table
            if self.loaded:
                self.ui.chromatogram_table.setEnabled(True)

                # The brackets
                for i in range(len(self.compound_names)):
                    channel = int(self.compound_data[self.compound_names[i]][7])
                    detector = int(self.compound_data[self.compound_names[i]][8])

                    # Channel 1 FF
                    if channel == 1 and detector == 1:
                        self.ui.Ch1_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][0][0], [0, max(self.Ch1_FF) * 0.1], 'k', linestyle='dotted')
                        self.ui.Ch1_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][1][0], [0, max(self.Ch1_FF) * 0.1], 'r', linestyle='dotted')

                    # Channel 2 FF
                    elif channel == 2 and detector == 1:
                        if float(self.compound_data[self.compound_names[i]][5]) > 0:
                            self.ui.Ch2_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][0][0], [0, max(self.Ch2_FF) * 0.1], 'k', linestyle='dotted')
                            self.ui.Ch2_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][1][0], [0, max(self.Ch2_FF) * 0.1], 'r', linestyle='dotted')

                    # Channel 2 BF
                    elif channel == 2 and detector == 2:
                        if float(self.compound_data[self.compound_names[i]][5]) > 0:
                            self.ui.Ch2_BF.canvas.ax.plot(self.brackets[self.compound_names[i]][0][0], [0, (abs(min(self.Ch2_BF)) + max(self.Ch2_BF))
                                                                                                        * 0.1], 'k', linestyle='dotted')
                            self.ui.Ch2_BF.canvas.ax.plot(self.brackets[self.compound_names[i]][1][0], [0, (abs(min(self.Ch2_BF)) + max(self.Ch2_BF))
                                                                                                        * 0.1], 'r', linestyle='dotted')

            if draw:
                # Showing the plots
                self.ui.Ch1_FF.canvas.draw(), self.ui.Ch2_FF.canvas.draw(), self.ui.Ch2_BF.canvas.draw()
                self.ui.mass_spectrum.canvas.draw(), self.ui.electron_image.canvas.draw()

        else:
            self.ui.Ch1_FF.setEnabled(False), self.ui.Ch2_FF.setEnabled(False), self.ui.Ch2_BF.setEnabled(False)
            self.ui.mass_spectrum.setEnabled(False), self.ui.electron_image.setEnabled(False)

            # Clearing plots and redrawing them
            self.ui.Ch1_FF.canvas.ax.clear(), self.ui.Ch1_FF.canvas.draw()
            self.ui.Ch2_FF.canvas.ax.clear(), self.ui.Ch2_FF.canvas.draw()
            self.ui.Ch2_BF.canvas.ax.clear(), self.ui.Ch2_BF.canvas.draw()
            self.ui.mass_spectrum.canvas.ax.clear(), self.ui.mass_spectrum.canvas.draw()
            self.ui.electron_image.canvas.ax.clear(), self.ui.electron_image.canvas.draw()

    # When the chromatogram is double-clicked, the event below will execute
    def plot_click(self, event):
        if self.ui.line_box.isChecked():
            if event.dblclick:
                try:
                    # Enabling the mass_spectrum and electron_image plots
                    self.ui.mass_spectrum.setEnabled(True), self.ui.electron_image.setEnabled(True)

                    # Location of the plot click and creating the position for the line
                    ix = round(float(event.xdata), 2)
                    line_x = self.time[np.where(self.time == ix)[0][0]]

                    # Refreshing the plots by plotting only the data
                    self.plots(draw=False)

                    # Plotting the line and time marker
                    self.ui.Ch1_FF.canvas.ax.plot([line_x, line_x], [min(self.Ch1_FF), max(self.Ch1_FF)], 'y')
                    self.ui.Ch2_FF.canvas.ax.plot([line_x, line_x], [min(self.Ch2_FF), max(self.Ch2_FF)], 'y')
                    self.ui.Ch2_BF.canvas.ax.plot([line_x, line_x], [min(self.Ch2_BF), max(self.Ch2_BF)], 'y')
                    self.ui.Ch1_FF.canvas.fig.text(ix, max(self.Ch1_FF), str(f'{ix} min'), transform=self.ui.Ch1_FF.canvas.ax.transData)
                    self.ui.Ch2_FF.canvas.fig.text(ix, max(self.Ch2_FF), str(f'{ix} min'), transform=self.ui.Ch2_FF.canvas.ax.transData)
                    self.ui.Ch2_BF.canvas.fig.text(ix, max(self.Ch2_BF), str(f'{ix} min'), transform=self.ui.Ch2_BF.canvas.ax.transData)

                    # Setting the limits for the scales of the plots
                    if self.x1 != self.x2 or self.y1 != self.y2:
                        self.ui.Ch1_FF.canvas.ax.set_xlim([min(self.Ch1_FF_x1, self.Ch1_FF_x2), max(self.Ch1_FF_x1, self.Ch1_FF_x2)])
                        self.ui.Ch1_FF.canvas.ax.set_ylim([min(self.Ch1_FF_y1, self.Ch1_FF_y2), max(self.Ch1_FF_y1, self.Ch1_FF_y2)])
                        self.ui.Ch2_FF.canvas.ax.set_xlim([min(self.Ch2_FF_x1, self.Ch2_FF_x2), max(self.Ch2_FF_x1, self.Ch2_FF_x2)])
                        self.ui.Ch2_FF.canvas.ax.set_ylim([min(self.Ch2_FF_y1, self.Ch2_FF_y2), max(self.Ch2_FF_y1, self.Ch2_FF_y2)])
                        self.ui.Ch2_BF.canvas.ax.set_xlim([min(self.Ch2_BF_x1, self.Ch2_BF_x2), max(self.Ch2_BF_x1, self.Ch2_BF_x2)])
                        self.ui.Ch2_BF.canvas.ax.set_ylim([min(self.Ch2_BF_y1, self.Ch2_BF_y2), max(self.Ch2_BF_y1, self.Ch2_BF_y2)])

                    # Drawing the plots
                    self.ui.Ch1_FF.canvas.draw(), self.ui.Ch2_FF.canvas.draw(), self.ui.Ch2_BF.canvas.draw()
                    self.ui.mass_spectrum.canvas.ax.clear(), self.ui.electron_image.canvas.ax.clear()

                    # Comparing mass spectrum with nist database and doing a conversion from time to m/z
                    mz, ampl, nist_data = tof.tof_select('Data/scan_example.h5', ix)

                    # The comparison below needs more data files, it has only 1 at this moment
                    for i in range(len(nist_data)):
                        self.ui.mass_spectrum.canvas.ax.bar(nist_data[i][0], -nist_data[i][1], label='NIST database', color='r')

                    self.ui.mass_spectrum.canvas.ax.plot(mz, ampl, "k-", label='Experiment')

                    # The * 0.5 below is a temporary correction
                    self.ui.mass_spectrum.canvas.ax.set(xlim=(np.min(mz), 0.5 * np.max(mz)), xlabel='m/z', ylabel='Counts')
                    self.ui.mass_spectrum.canvas.ax.legend(loc='best')
                    self.ui.mass_spectrum.canvas.ax.set_title(f'Mass spectrum at {ix} min')
                    self.ui.mass_spectrum.canvas.ax.grid(True, 'both')
                    self.ui.mass_spectrum.canvas.draw()

                    # Selecting the electron image based on which location of the plot has been clicked
                    with h5py.File('Data/example.h5', 'r') as f:
                        picture_nr = round(abs(round(ix)) / max(self.time) * 9)
                        electron_list = list(f.keys())[0]
                        electron_images = f[electron_list][()]
                        self.ui.electron_image.canvas.ax.imshow(electron_images[picture_nr])
                        self.ui.electron_image.canvas.ax.axis('off')
                        self.ui.electron_image.canvas.ax.set_title(f'Electron image at {ix} min')
                        self.ui.electron_image.canvas.draw()
                        self.ix = ix

                except Exception as e:
                    self.warning_window = WarningWindow(text=e)

        # The zoom in function per graph
        if self.ui.zoom_box.isChecked():
            try:
                if self.first_click:
                    self.x1, self.y1 = event.xdata, event.ydata
                    if isinstance(self.x1, float) and isinstance(self.y1, float):
                        self.first_click = False
                        if self.ui.Ch1_FF_tab.isVisible():
                            self.Ch1_FF_x1, self.Ch1_FF_y1 = event.xdata, event.ydata
                        elif self.ui.Ch2_FF_tab.isVisible():
                            self.Ch2_FF_x1, self.Ch2_FF_y1 = event.xdata, event.ydata
                        elif self.ui.Ch2_BF_tab.isVisible():
                            self.Ch2_BF_x1, self.Ch2_BF_y1 = event.xdata, event.ydata

                else:
                    self.x2, self.y2 = event.xdata, event.ydata
                    self.first_click = True
                    if isinstance(self.x2, float) and isinstance(self.y2, float):
                        if self.ui.Ch1_FF_tab.isVisible():
                            self.Ch1_FF_x2, self.Ch1_FF_y2 = event.xdata, event.ydata
                        elif self.ui.Ch2_FF_tab.isVisible():
                            self.Ch2_FF_x2, self.Ch2_FF_y2 = event.xdata, event.ydata
                        elif self.ui.Ch2_BF_tab.isVisible():
                            self.Ch2_BF_x2, self.Ch2_BF_y2 = event.xdata, event.ydata

                    if self.x1 != self.x2 or self.y1 != self.y2:
                        if self.ui.Ch1_FF_tab.isVisible():
                            self.ui.Ch1_FF.canvas.ax.set_xlim([min(self.Ch1_FF_x1, self.Ch1_FF_x2), max(self.Ch1_FF_x1, self.Ch1_FF_x2)])
                            self.ui.Ch1_FF.canvas.ax.set_ylim([min(self.Ch1_FF_y1, self.Ch1_FF_y2), max(self.Ch1_FF_y1, self.Ch1_FF_y2)])
                            self.ui.Ch1_FF.canvas.draw()

                        elif self.ui.Ch2_FF_tab.isVisible():
                            self.ui.Ch2_FF.canvas.ax.set_xlim([min(self.Ch2_FF_x1, self.Ch2_FF_x2), max(self.Ch2_FF_x1, self.Ch2_FF_x2)])
                            self.ui.Ch2_FF.canvas.ax.set_ylim([min(self.Ch2_FF_y1, self.Ch2_FF_y2), max(self.Ch2_FF_y1, self.Ch2_FF_y2)])
                            self.ui.Ch2_FF.canvas.draw()

                        elif self.ui.Ch2_BF_tab.isVisible():
                            self.ui.Ch2_BF.canvas.ax.set_xlim([min(self.Ch2_BF_x1, self.Ch2_BF_x2), max(self.Ch2_BF_x1, self.Ch2_BF_x2)])
                            self.ui.Ch2_BF.canvas.ax.set_ylim([min(self.Ch2_BF_y1, self.Ch2_BF_y2), max(self.Ch2_BF_y1, self.Ch2_BF_y2)])
                            self.ui.Ch2_BF.canvas.draw()

                    else:
                        pass

            except Exception as e:
                self.warning_window = WarningWindow(text=e)

    # The function to apply a line
    def line(self):
        if self.ui.line_box.isChecked():
            self.ui.line_box.setChecked(True)
            self.ui.zoom_box.setChecked(False)

    # The function to apply a zoom
    def zoom(self):
        if self.ui.zoom_box.isChecked():
            self.ui.line_box.setChecked(False)
            self.ui.zoom_box.setChecked(True)

    # Reset the zoom in of the visible chromatograms
    def reset_chromatograms(self):
        if self.ui.Ch1_FF_tab.isVisible():
            self.Ch1_FF_x1, self.Ch1_FF_x2 = min(self.time) - max(self.time) * 0.05, max(self.time) + max(self.time) * 0.05
            self.Ch1_FF_y1, self.Ch1_FF_y2 = min(self.Ch1_FF) - max(self.Ch1_FF) * 0.05, max(self.Ch1_FF) + max(self.Ch1_FF) * 0.05
            self.ui.Ch1_FF.canvas.ax.set_xlim([self.Ch1_FF_x1, self.Ch1_FF_x2])
            self.ui.Ch1_FF.canvas.ax.set_ylim([self.Ch1_FF_y1, self.Ch1_FF_y2])
            self.ui.Ch1_FF.canvas.draw()

        elif self.ui.Ch2_FF_tab.isVisible():
            self.Ch2_FF_x1, self.Ch2_FF_x2 = min(self.time) - max(self.time) * 0.05, max(self.time) + max(self.time) * 0.05
            self.Ch2_FF_y1, self.Ch2_FF_y2 = min(self.Ch2_FF) - max(self.Ch2_FF) * 0.05, max(self.Ch2_FF) + max(self.Ch2_FF) * 0.05
            self.ui.Ch2_FF.canvas.ax.set_xlim([self.Ch2_FF_x1, self.Ch2_FF_x2])
            self.ui.Ch2_FF.canvas.ax.set_ylim([self.Ch2_FF_y1, self.Ch2_FF_y2])
            self.ui.Ch2_FF.canvas.draw()

        elif self.ui.Ch2_BF_tab.isVisible():
            self.Ch2_BF_x1, self.Ch2_BF_x2 = min(self.time) - max(self.time) * 0.05, max(self.time) + max(self.time) * 0.05
            self.Ch2_BF_y1, self.Ch2_BF_y2 = min(self.Ch2_BF) - max(self.Ch2_BF) * 0.05, max(self.Ch2_BF) + max(self.Ch2_BF) * 0.05
            self.ui.Ch2_BF.canvas.ax.set_xlim([self.Ch2_BF_x1, self.Ch2_BF_x2])
            self.ui.Ch2_BF.canvas.ax.set_ylim([self.Ch2_BF_y1, self.Ch2_BF_y2])
            self.ui.Ch2_BF.canvas.draw()

    # The table interaction of compounds
    def table_click(self):
        self.plots(draw=False)
        index = self.ui.chromatogram_table.currentRow()
        channel = int(self.compound_data[self.compound_names[index]][7])
        detector = int(self.compound_data[self.compound_names[index]][8])
        x = float(self.compound_data[self.compound_names[index]][1])

        if x != 0:
            if channel == 1 and detector == 1:
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.Ch1_FF.canvas.ax.plot([x, x], [min(self.Ch1_FF), max(self.Ch1_FF)], 'grey', linestyle='dotted')
                self.ui.Ch1_FF.canvas.fig.text(x, max(self.Ch1_FF), self.compound_names[index], transform=self.ui.Ch1_FF.canvas.ax.transData, color='red')
                self.ui.Ch1_FF.canvas.draw()

            elif channel == 2 and detector == 1:
                self.ui.tabWidget.setCurrentIndex(1)
                self.ui.Ch2_FF.canvas.ax.plot([x, x], [min(self.Ch2_FF), max(self.Ch2_FF)], 'grey', linestyle='dotted')
                self.ui.Ch2_FF.canvas.fig.text(x, max(self.Ch2_FF), self.compound_names[index], transform=self.ui.Ch2_FF.canvas.ax.transData, color='red')
                self.ui.Ch2_FF.canvas.draw()

            elif channel == 2 and detector == 2:
                self.ui.tabWidget.setCurrentIndex(2)
                self.ui.Ch2_BF.canvas.ax.plot([x, x], [min(self.Ch2_BF), max(self.Ch2_BF)], 'grey', linestyle='dotted')
                self.ui.Ch2_BF.canvas.fig.text(x, max(self.Ch2_BF), self.compound_names[index], transform=self.ui.Ch2_BF.canvas.ax.transData, color='red')
                self.ui.Ch2_BF.canvas.draw()

    # The function that creates a separate window in which the electron image is visible
    def electron_image_click(self, event):
        if event.dblclick:
            self.ui_EC = ElectronImageController(self.time, self.ix)

    # The function to open the micro GC window
    def open_micro_gc_window(self):
        self.window_GC = MicroGcController()


# The hard workers, also known as the threads
class Worker1(QObject):
    finished1, progress1 = pyqtSignal(), pyqtSignal(int)

    def run(self):
        while check:
            self.progress1.emit(1)
            sleep(1)
        self.finished1.emit()

# class Worker2(QObject):
#     finished2 = pyqtSignal()
#     progress2 = pyqtSignal(int)
#
#     def run(self):
#         while v.check2 is True:
#             tb = time()
#             sleep(1)
#             te = time()
#             sleep(1 - (te - tb))  # Getting a more accurate than sleep(1)
#             self.progress2.emit(v.i2 + 1)
#         self.finished2.emit()
