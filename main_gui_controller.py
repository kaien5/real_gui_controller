import os
import h5py
import numpy as np
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder

import file_browser
import dynamiq_import
import hvc_controller
import motor_controller

from time import sleep
from PyQt5 import QtWidgets
from main_gui import Ui_MainWindow
from pymodbus.client.sync import ModbusTcpClient
from microGC_controller import MicroGcController
from injector_controller import Injector_controller
from PyQt5.QtCore import QObject, pyqtSignal, QThread

check = True


class Controller:
    def __init__(self, load=False, data=None):
        self.wait = None
        self.client = None
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

        # The chromatogram and mass spectrum settings
        self.ui.chromatogram1.canvas.fig.suptitle('Ch1 (FF)')
        self.ui.chromatogram2.canvas.fig.suptitle('Ch2 (FF)')
        self.ui.chromatogram3.canvas.fig.suptitle('Ch3 (BF)')
        self.ui.mass_spectrum.canvas.fig.suptitle('Mass spectrum')
        self.ui.electron_image.canvas.fig.suptitle('Electron image')
        self.ui.chromatogram1.canvas.mpl_connect('button_press_event', self.on_click)
        self.ui.chromatogram2.canvas.mpl_connect('button_press_event', self.on_click)
        self.ui.chromatogram3.canvas.mpl_connect('button_press_event', self.on_click)
        self.ui.chromatogram1.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.chromatogram1.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.chromatogram2.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.chromatogram2.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.chromatogram3.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.chromatogram3.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.mass_spectrum.canvas.fig.text(0.85, 0.05, 'Index nr.', ha='center', va='center')
        self.ui.mass_spectrum.canvas.fig.text(0.05, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')

        # Disabling the plots at start up
        self.ui.chromatogram1.setEnabled(False)
        self.ui.chromatogram2.setEnabled(False)
        self.ui.chromatogram3.setEnabled(False)
        self.ui.mass_spectrum.setEnabled(False)
        self.ui.electron_image.setEnabled(False)

        # Load data from supplied file, else demo file
        if load:
            self.time = data[0]
            self.Ch1_FF = data[1]
            self.Ch2_FF = data[2]
            self.Ch3_BF = data[3]
        else:
            file_name = os.getcwd() + '/Data/Demo_file.txt'
            self.ui.chromatogram1.canvas.fig.suptitle('Demo Data')
            self.ui.chromatogram2.canvas.fig.suptitle('Demo Data')
            self.ui.chromatogram3.canvas.fig.suptitle('Demo Data')
            self.ui.mass_spectrum.canvas.fig.suptitle('Demo Data')
            self.ui.electron_image.canvas.fig.suptitle('Demo Data')
            self.time = np.loadtxt(file_name, skiprows=3, usecols=0)
            self.Ch1_FF = np.loadtxt(file_name, skiprows=3, usecols=1)
            self.Ch2_FF = np.loadtxt(file_name, skiprows=3, usecols=2)
            self.Ch3_BF = np.loadtxt(file_name, skiprows=3, usecols=3)

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
                self.sequence_names['Sequence ' + str(i + 1)] = decoder.decode_string(20).decode()

            self.client.close()
            self.ui.sequence_label.setText(self.sequence_names['Sequence ' + str(self.ui.sequence_number.value())])

            if self.ui.start_button.isEnabled() is False:
                self.ui.start_button.setEnabled(True)

            if self.ui.sequence_number.isEnabled() is False:
                self.ui.sequence_number.setEnabled(True)

        except:
            self.ui.microGC_status.setText('Invalid IP Address')

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
        microGC_ip = self.ui.ip_address_microGC.text()
        self.filename = dynamiq_import.load(host=microGC_ip, port=7197)
        self.ui.chromatogram1.canvas.fig.suptitle('Ch1 (FF)')
        self.ui.chromatogram2.canvas.fig.suptitle('Ch2 (FF)')
        self.ui.chromatogram3.canvas.fig.suptitle('Ch3 (BF)')
        self.ui.mass_spectrum.canvas.fig.suptitle('Mass spectrum')
        self.ui.electron_image.canvas.fig.suptitle('Electron image')
        self.time = np.loadtxt(str(self.filename), skiprows=3, usecols=0)
        self.Ch1_FF = np.loadtxt(str(self.filename), skiprows=3, usecols=1)
        self.Ch2_FF = np.loadtxt(str(self.filename), skiprows=3, usecols=2)
        self.Ch3_BF = np.loadtxt(str(self.filename), skiprows=3, usecols=3)

        if self.ui.enable_plots.isChecked():
            self.ui.enable_plots.toggle()
            self.ui.enable_plots.toggle()

        if self.ui.enable_plots.isChecked() is False:
            self.ui.enable_plots.toggle()

    def plots(self):
        # Based on the checkbox, the plots will be enabled or disabled
        if self.ui.enable_plots.checkState():
            if self.ui.chromatogram1.isEnabled() is False:
                self.ui.chromatogram1.setEnabled(True)
            if self.ui.chromatogram2.isEnabled() is False:
                self.ui.chromatogram2.setEnabled(True)
            if self.ui.chromatogram3.isEnabled() is False:
                self.ui.chromatogram3.setEnabled(True)
            if self.ui.mass_spectrum.isEnabled() is False:
                self.ui.mass_spectrum.setEnabled(True)
            if self.ui.electron_image.isEnabled() is False:
                self.ui.electron_image.setEnabled(True)

            # Plotting the chromatograms
            self.ui.chromatogram1.canvas.ax.clear()
            self.ui.chromatogram2.canvas.ax.clear()
            self.ui.chromatogram3.canvas.ax.clear()
            self.ui.chromatogram1.canvas.ax.plot(self.time, self.Ch1_FF)
            self.ui.chromatogram2.canvas.ax.plot(self.time, self.Ch2_FF)
            self.ui.chromatogram3.canvas.ax.plot(self.time, self.Ch3_BF)
            self.ui.chromatogram1.canvas.draw()
            self.ui.chromatogram2.canvas.draw()
            self.ui.chromatogram3.canvas.draw()

        else:
            if self.ui.chromatogram1.isEnabled():
                self.ui.chromatogram1.setEnabled(False)
            if self.ui.chromatogram2.isEnabled():
                self.ui.chromatogram2.setEnabled(False)
            if self.ui.chromatogram3.isEnabled():
                self.ui.chromatogram3.setEnabled(False)
            if self.ui.mass_spectrum.isEnabled():
                self.ui.mass_spectrum.setEnabled(False)
            if self.ui.electron_image.isEnabled():
                self.ui.electron_image.setEnabled(False)

            # Clearing plots and redrawing them
            self.ui.chromatogram1.canvas.ax.clear()
            self.ui.chromatogram1.canvas.draw()
            self.ui.chromatogram2.canvas.ax.clear()
            self.ui.chromatogram2.canvas.draw()
            self.ui.chromatogram3.canvas.ax.clear()
            self.ui.chromatogram3.canvas.draw()
            self.ui.mass_spectrum.canvas.ax.clear()
            self.ui.mass_spectrum.canvas.draw()
            self.ui.electron_image.canvas.ax.clear()
            self.ui.electron_image.canvas.draw()

    # When the chromatogram is double-clicked, the event below will execute
    def on_click(self, event):
        if event.dblclick:
            try:
                ix = round(float(event.xdata), 2)  # Location of the plot click
                index = np.where(self.time == ix)[0][0]  # Index location on where the line_x should appear
                line_x = self.time[index]
                self.ui.chromatogram1.canvas.ax.clear()
                self.ui.chromatogram2.canvas.ax.clear()
                self.ui.chromatogram3.canvas.ax.clear()
                self.ui.chromatogram1.canvas.ax.plot(self.time, self.Ch1_FF)
                self.ui.chromatogram2.canvas.ax.plot(self.time, self.Ch2_FF)
                self.ui.chromatogram3.canvas.ax.plot(self.time, self.Ch3_BF)
                self.ui.chromatogram1.canvas.ax.plot([line_x, line_x], [min(self.Ch1_FF), max(self.Ch1_FF)])
                self.ui.chromatogram2.canvas.ax.plot([line_x, line_x], [min(self.Ch2_FF), max(self.Ch2_FF)])
                self.ui.chromatogram3.canvas.ax.plot([line_x, line_x], [min(self.Ch3_BF), max(self.Ch3_BF)])
                self.ui.chromatogram1.canvas.draw()
                self.ui.chromatogram2.canvas.draw()
                self.ui.chromatogram3.canvas.draw()
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
            sleep(2)
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
