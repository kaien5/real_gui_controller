import os
import h5py
import struct
import numpy as np
import file_browser
import dynamiq_import
import hvc_controller
import motor_controller

from time import sleep
from PyQt5 import QtWidgets
from main_gui import Ui_MainWindow
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient
from microGC_controller import MicroGcController
from pymodbus.payload import BinaryPayloadDecoder
from injector_controller import Injector_controller
from PyQt5.QtCore import QObject, pyqtSignal, QThread

check = True


class Controller:
    def __init__(self, load=False, data=None):
        self.wait = None
        self.client = None
        self.loaded = False
        self.worker1 = None
        self.thread1 = None
        self.filename = None
        self.window_in = None
        self.window_GC = None
        self.window_hvc = None
        self.window_motor = None
        self.sequence_names = None
        self.fileBrowserWidget = None
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        # Maximizing the screen
        self.MainWindow.showMaximized()

        # The buttons and their functions
        self.ui.injector_settings_button.clicked.connect(self.open_injector_window)
        self.ui.microGC_settings_button.clicked.connect(self.open_micro_gc_window)
        self.ui.sequence_number.valueChanged.connect(self.sequence_selection)
        self.ui.motor_settings_button.clicked.connect(self.open_motor_window)
        self.ui.hvc_settings_button.clicked.connect(self.open_hvc_window)
        self.ui.action_Open.triggered.connect(self.open_file)
        self.ui.refresh_button.clicked.connect(self.refresh)
        self.ui.load_button.clicked.connect(self.load_data)
        self.ui.start_button.clicked.connect(self.start)
        self.ui.enable_plots.toggled.connect(self.plots)
        self.ui.stop_button.clicked.connect(self.stop)

        # Clicked on functions
        self.ui.ch1_FF.canvas.mpl_connect('button_press_event', self.plot_click)
        self.ui.ch2_FF.canvas.mpl_connect('button_press_event', self.plot_click)
        self.ui.ch2_BF.canvas.mpl_connect('button_press_event', self.plot_click)
        self.ui.chromatogram_table.clicked.connect(self.table_click)

        # The chromatogram and mass spectrum settings
        self.ui.ch1_FF.canvas.fig.suptitle('Ch1 (FF)')
        self.ui.ch2_FF.canvas.fig.suptitle('Ch2 (FF)')
        self.ui.ch2_BF.canvas.fig.suptitle('Ch2 (BF)')
        self.ui.mass_spectrum.canvas.fig.suptitle('Mass spectrum')
        self.ui.electron_image.canvas.fig.suptitle('Electron image')
        self.ui.ch1_FF.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.ch1_FF.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.ch2_FF.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.ch2_FF.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.ch2_BF.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.ch2_BF.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.mass_spectrum.canvas.fig.text(0.85, 0.05, 'Index nr.', ha='center', va='center')
        self.ui.mass_spectrum.canvas.fig.text(0.05, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')

        # Disabling the plots at start up
        self.ui.ch1_FF.setEnabled(False)
        self.ui.ch2_FF.setEnabled(False)
        self.ui.ch2_BF.setEnabled(False)
        self.ui.mass_spectrum.setEnabled(False)
        self.ui.electron_image.setEnabled(False)

        # Load data from supplied file, else demo file
        if load:
            self.time = data[0]
            self.Ch1_FF = data[1]
            self.Ch2_FF = data[2]
            self.Ch2_BF = data[3]
        else:
            file_name = os.getcwd() + '/Data/Demo_file.txt'
            self.ui.ch1_FF.canvas.fig.suptitle('Demo Data')
            self.ui.ch2_FF.canvas.fig.suptitle('Demo Data')
            self.ui.ch2_BF.canvas.fig.suptitle('Demo Data')
            self.ui.mass_spectrum.canvas.fig.suptitle('Demo Data')
            self.ui.electron_image.canvas.fig.suptitle('Demo Data')
            self.time = np.loadtxt(file_name, skiprows=3, usecols=0)
            self.Ch1_FF = np.loadtxt(file_name, skiprows=3, usecols=1)
            self.Ch2_FF = np.loadtxt(file_name, skiprows=3, usecols=2)
            self.Ch2_BF = np.loadtxt(file_name, skiprows=3, usecols=3)

    def sequence_selection(self):
        self.ui.sequence_label.setText(self.sequence_names['Sequence ' + str(self.ui.sequence_number.value())])

    # Start the data acquisition
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
            self.ui.refresh_button.setEnabled(False)
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

        except:
            self.ui.microGC_status.setText('Invalid IP Address')

    def stop(self):
        global check
        self.client.write_register(0x9D0A, 1)
        self.client.close()
        self.ui.refresh_button.setEnabled(False)
        self.ui.refresh_button.setEnabled(True)
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        check = False
        self.ui.microGC_status.setText('Run cancelled')

    def refresh(self):
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
            self.ui.start_button.setEnabled(True)
            self.ui.sequence_number.setEnabled(True)
            self.ui.load_button.setEnabled(True)

        except:
            self.ui.microGC_status.setText('No connection possible')

    # This is to check whether the MicroGC is busy
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
                self.ui.refresh_button.setEnabled(True)
                self.ui.stop_button.setEnabled(False)
                self.ui.start_button.setEnabled(True)
                self.ui.load_button.setEnabled(True)
                check = False
            self.client.close()

    def load_data(self):
        # Communicating to the plot function
        self.loaded = True

        # Connect to the IP written in the text line
        microGC_ip = self.ui.ip_address_microGC.text()
        self.filename = dynamiq_import.load(host=microGC_ip, port=7197)

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

        column_names = ['Concentration [mol%]', 'Retention time [sec]', 'Peak area [mV×sec]', 'Peak height [mV]', 'Peak width [sec]',
                        'Integration start [sec]', 'Integration end [sec]', 'Channel number [Ch]', 'Detector']

        # The horizontal headers
        for i in range(len(column_names)):
            if self.ui.chromatogram_table.columnCount() < len(column_names):
                self.ui.chromatogram_table.insertColumn(i)
                self.ui.chromatogram_table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem(column_names[i]))

        # The vertical headers
        for i in range(number_of_compounds):
            if self.ui.chromatogram_table.rowCount() < number_of_compounds:
                self.ui.chromatogram_table.insertRow(i)
            self.ui.chromatogram_table.setVerticalHeaderItem(i, QtWidgets.QTableWidgetItem(self.compound_names[i]))

        # The table contents
        for i in range(number_of_compounds):
            for _ in range(len(column_names)):
                if _ == 8:
                    if int(self.compound_data[self.compound_names[i]][_]) == 1:
                        self.ui.chromatogram_table.setItem(i, _, QtWidgets.QTableWidgetItem('FF'))
                    elif int(self.compound_data[self.compound_names[i]][_]) == 2:
                        self.ui.chromatogram_table.setItem(i, _, QtWidgets.QTableWidgetItem('BF'))

                else:
                    self.ui.chromatogram_table.setItem(i, _, QtWidgets.QTableWidgetItem(self.compound_data[self.compound_names[i]][_]))

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

        # Changing titles of the plots
        self.ui.ch1_FF.canvas.fig.suptitle('Ch1 (FF)')
        self.ui.ch2_FF.canvas.fig.suptitle('Ch2 (FF)')
        self.ui.ch2_BF.canvas.fig.suptitle('Ch2 (BF)')
        self.ui.mass_spectrum.canvas.fig.suptitle('Mass spectrum')
        self.ui.electron_image.canvas.fig.suptitle('Electron image')

        # The data for the plots
        self.time = np.loadtxt(str(self.filename), skiprows=3, usecols=0)
        self.Ch1_FF = np.loadtxt(str(self.filename), skiprows=3, usecols=1)
        self.Ch2_FF = np.loadtxt(str(self.filename), skiprows=3, usecols=2)
        self.Ch2_BF = np.loadtxt(str(self.filename), skiprows=3, usecols=3)

        # Refreshing the plots
        if self.ui.enable_plots.isChecked():
            self.ui.enable_plots.toggle()
            self.ui.enable_plots.toggle()
        else:
            self.ui.enable_plots.toggle()

        # Closing the connection to the client
        self.client.close()

    def plots(self, draw=True):
        # Based on the checkbox, the plots will be enabled or disabled
        if self.ui.enable_plots.checkState():
            self.ui.ch1_FF.setEnabled(True)
            self.ui.ch2_FF.setEnabled(True)
            self.ui.ch2_BF.setEnabled(True)
            self.ui.mass_spectrum.setEnabled(True)
            self.ui.electron_image.setEnabled(True)

            # Clearing the plots
            self.ui.ch1_FF.canvas.ax.clear()
            self.ui.ch2_FF.canvas.ax.clear()
            self.ui.ch2_BF.canvas.ax.clear()
            self.ui.ch1_FF.canvas.fig.texts.clear()
            self.ui.ch2_FF.canvas.fig.texts.clear()
            self.ui.ch2_BF.canvas.fig.texts.clear()
            self.ui.mass_spectrum.canvas.ax.clear()
            self.ui.electron_image.canvas.ax.clear()

            # Plotting the data and brackets
            self.ui.ch1_FF.canvas.ax.plot(self.time, self.Ch1_FF, 'b')
            self.ui.ch2_FF.canvas.ax.plot(self.time, self.Ch2_FF, 'b')
            self.ui.ch2_BF.canvas.ax.plot(self.time, self.Ch2_BF, 'b')

            if self.loaded:
                # Enabling the chromatogram table
                self.ui.chromatogram_table.setEnabled(True)

                # The brackets
                for i in range(len(self.compound_names)):
                    channel = int(self.compound_data[self.compound_names[i]][7])
                    detector = int(self.compound_data[self.compound_names[i]][8])

                    # Channel 1 FF
                    if channel == 1 and detector == 1:
                        self.ui.ch1_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][0][0],
                                                      [0, max(self.Ch1_FF) * 0.1], 'k', linestyle='dotted')
                        self.ui.ch1_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][1][0],
                                                      [0, max(self.Ch1_FF) * 0.1], 'r', linestyle='dotted')

                    # Channel 2 FF
                    elif channel == 2 and detector == 1:
                        if float(self.compound_data[self.compound_names[i]][5]) > 0:
                            self.ui.ch2_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][0][0],
                                                          [0, max(self.Ch2_FF) * 0.1], 'k', linestyle='dotted')
                            self.ui.ch2_FF.canvas.ax.plot(self.brackets[self.compound_names[i]][1][0],
                                                          [0, max(self.Ch2_FF) * 0.1], 'r', linestyle='dotted')

                    # Channel 2 BF
                    elif channel == 2 and detector == 2:
                        if float(self.compound_data[self.compound_names[i]][5]) > 0:
                            self.ui.ch2_BF.canvas.ax.plot(self.brackets[self.compound_names[i]][0][0], [0, (abs(min(self.Ch2_BF)) + max(self.Ch2_BF))
                                                                                                        * 0.1], 'k', linestyle='dotted')
                            self.ui.ch2_BF.canvas.ax.plot(self.brackets[self.compound_names[i]][1][0], [0, (abs(min(self.Ch2_BF)) + max(self.Ch2_BF))
                                                                                                        * 0.1], 'r', linestyle='dotted')

            if draw:
                # Showing the plots
                self.ui.ch1_FF.canvas.draw()
                self.ui.ch2_FF.canvas.draw()
                self.ui.ch2_BF.canvas.draw()
                self.ui.mass_spectrum.canvas.draw()
                self.ui.electron_image.canvas.draw()

        else:
            self.ui.ch1_FF.setEnabled(False)
            self.ui.ch2_FF.setEnabled(False)
            self.ui.ch2_BF.setEnabled(False)
            self.ui.mass_spectrum.setEnabled(False)
            self.ui.electron_image.setEnabled(False)

            # Clearing plots and redrawing them
            self.ui.ch1_FF.canvas.ax.clear()
            self.ui.ch1_FF.canvas.draw()
            self.ui.ch2_FF.canvas.ax.clear()
            self.ui.ch2_FF.canvas.draw()
            self.ui.ch2_BF.canvas.ax.clear()
            self.ui.ch2_BF.canvas.draw()
            self.ui.mass_spectrum.canvas.ax.clear()
            self.ui.mass_spectrum.canvas.draw()
            self.ui.electron_image.canvas.ax.clear()
            self.ui.electron_image.canvas.draw()

    # When the chromatogram is double-clicked, the event below will execute
    def plot_click(self, event):
        print(event.xdata, event.ydata)  # TODO Create zoom function

        if event.dblclick:
            try:
                ix = round(float(event.xdata), 2)  # Location of the plot click
                index = np.where(self.time == ix)[0][0]  # Index location on where the line_x should appear
                line_x = self.time[index]

                self.plots(draw=False)
                self.ui.ch1_FF.canvas.ax.plot([line_x, line_x], [min(self.Ch1_FF), max(self.Ch1_FF)], 'y')
                self.ui.ch2_FF.canvas.ax.plot([line_x, line_x], [min(self.Ch2_FF), max(self.Ch2_FF)], 'y')
                self.ui.ch2_BF.canvas.ax.plot([line_x, line_x], [min(self.Ch2_BF), max(self.Ch2_BF)], 'y')

                self.ui.ch1_FF.canvas.draw()
                self.ui.ch2_FF.canvas.draw()
                self.ui.ch2_BF.canvas.draw()
                self.ui.mass_spectrum.canvas.ax.clear()

                # Selecting the TOF file based on which location of the plot has been clicked
                with h5py.File('Data/scan_example.h5', 'r') as f:
                    tof_list = list(f.keys())[0]

                    # Creating a list for the files in TOF
                    x = []
                    for _ in f[tof_list]:
                        x.append(_)

                    tof_nr = f[tof_list][x[abs(round(ix))]]
                    tof = np.squeeze(tof_nr['TOF0'])
                    self.ui.mass_spectrum.canvas.ax.plot(tof)
                    self.ui.mass_spectrum.canvas.draw()

                # Selecting the electron image based on which location of the plot has been clicked
                with h5py.File('Data/example.h5', 'r') as f:
                    picture_nr = round(abs(round(ix)) / max(self.time) * 9)
                    electron_list = list(f.keys())[0]
                    electron_images = f[electron_list][()]
                    self.ui.electron_image.canvas.ax.imshow(electron_images[picture_nr])
                    self.ui.electron_image.canvas.draw()

            except Exception as e:
                print(f'Click inside the boundaries because the {e}')

    def table_click(self):
        self.plots(draw=False)
        index = self.ui.chromatogram_table.currentRow()
        channel = int(self.compound_data[self.compound_names[index]][7])
        detector = int(self.compound_data[self.compound_names[index]][8])
        x = float(self.compound_data[self.compound_names[index]][1])

        if x != 0:
            if channel == 1 and detector == 1:
                self.ui.tabWidget.setCurrentIndex(0)
                self.ui.ch1_FF.canvas.ax.plot([x, x], [min(self.Ch1_FF), max(self.Ch1_FF)], 'grey', linestyle='dotted')
                self.ui.ch1_FF.canvas.fig.text(x, max(self.Ch1_FF), self.compound_names[index], transform=self.ui.ch1_FF.
                                               canvas.ax.transData, color='red')

            elif channel == 2 and detector == 1:
                self.ui.tabWidget.setCurrentIndex(1)
                self.ui.ch2_FF.canvas.ax.plot([x, x], [min(self.Ch2_FF), max(self.Ch2_FF)], 'grey', linestyle='dotted')
                self.ui.ch2_FF.canvas.fig.text(x, max(self.Ch2_FF), self.compound_names[index], transform=self.ui.
                                               ch2_FF.canvas.ax.transData, color='red')

            elif channel == 2 and detector == 2:
                self.ui.tabWidget.setCurrentIndex(2)
                self.ui.ch2_BF.canvas.ax.plot([x, x], [min(self.Ch2_BF), max(self.Ch2_BF)], 'grey', linestyle='dotted')
                self.ui.ch2_BF.canvas.fig.text(x, max(self.Ch2_BF), self.compound_names[index], transform=self.ui.ch2_BF.canvas.ax.transData,
                                               color='red')

        self.ui.ch1_FF.canvas.draw()
        self.ui.ch2_FF.canvas.draw()
        self.ui.ch2_BF.canvas.draw()

    # The function to open the injector window
    def open_injector_window(self):
        self.window_in = Injector_controller()

    # The function to open the micro GC window
    def open_micro_gc_window(self):
        self.window_GC = MicroGcController()

    def open_hvc_window(self):
        self.window_hvc = hvc_controller.HvcController()

    def open_motor_window(self):
        self.window_motor = motor_controller.MotorController()

    def open_file(self):
        self.MainWindow.close()
        self.fileBrowserWidget = file_browser.FileBrowserController(open_file=True, main=True)
        self.fileBrowserWidget.show()
        self.fileBrowserWidget.set_path()


# The hard workers, also known as the threads
class Worker1(QObject):
    finished1 = pyqtSignal()
    progress1 = pyqtSignal(int)

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
