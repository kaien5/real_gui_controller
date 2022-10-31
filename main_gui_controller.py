import os
import h5py
import numpy as np
import file_browser

from PyQt5 import QtWidgets
from chiralMS_controller import ChiralMsController
from injector_controller import Injector_controller
from microGC_controller import MicroGcController
from main_gui import Ui_MainWindow

# from time import time, sleep
# from PyQt5.QtCore import QObject, pyqtSignal


class Controller:
    def __init__(self, load=False, data=None):
        self.window_in = None
        self.window_GC = None
        self.window_MS = None
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
        self.ui.chiralMS_settings_button.clicked.connect(self.open_chiral_ms_window)
        self.ui.action_Open.triggered.connect(self.open_file)

        # # The start and stop button
        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.stop)

        # The chromatogram and mass spectrum settings
        self.ui.chromatogram1.canvas.fig.suptitle('Ch1 (FF)')
        self.ui.chromatogram2.canvas.fig.suptitle('Ch2 (FF)')
        self.ui.mass_spectrum.canvas.fig.suptitle('Mass spectrum')
        self.ui.electron_image.canvas.fig.suptitle('Electron image')
        self.ui.chromatogram1.canvas.mpl_connect('button_press_event', self.on_click)
        self.ui.chromatogram2.canvas.mpl_connect('button_press_event', self.on_click)
        self.ui.chromatogram1.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.chromatogram1.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.chromatogram2.canvas.fig.text(0.84, 0.05, 'Retention time (min)', ha='center', va='center')
        self.ui.chromatogram2.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.mass_spectrum.canvas.fig.text(0.85, 0.05, 'Index nr.', ha='center', va='center')
        self.ui.mass_spectrum.canvas.fig.text(0.05, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')

        # Load data from supplied file, else demo file
        if load:
            self.ui.demo_label.hide()
            self.test_file_time = data[0]
            self.test_file_Ch1_FF_intensity = data[1]
            self.test_file_Ch2_FF_intensity = data[2]
        else:
            self.ui.demo_label.show()
            file_name = os.getcwd() + '/Files/Demo_file.txt'
            self.test_file_time = np.loadtxt(file_name, skiprows=3, usecols=0)
            self.test_file_Ch1_FF_intensity = np.loadtxt(file_name, skiprows=3, usecols=1)
            self.test_file_Ch2_FF_intensity = np.loadtxt(file_name, skiprows=3, usecols=5)

    # Start the data acquisition
    def start(self):
        # Disabling and enabling the buttons and plots
        self.ui.start_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)
        self.ui.chromatogram1.setEnabled(True)
        self.ui.chromatogram2.setEnabled(True)
        self.ui.mass_spectrum.setEnabled(True)
        self.ui.electron_image.setEnabled(True)

        # Plotting the chromatograms
        self.ui.chromatogram1.canvas.ax.clear()
        self.ui.chromatogram2.canvas.ax.clear()
        self.ui.chromatogram1.canvas.ax.plot(self.test_file_time, self.test_file_Ch1_FF_intensity)
        self.ui.chromatogram2.canvas.ax.plot(self.test_file_time, self.test_file_Ch2_FF_intensity)
        self.ui.chromatogram1.canvas.draw()
        self.ui.chromatogram2.canvas.draw()

    # Stop the data acquisition
    def stop(self):
        # Enabling, disabling and clearing plots
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        self.ui.chromatogram1.canvas.ax.clear()
        self.ui.chromatogram1.canvas.draw()
        self.ui.chromatogram1.setEnabled(False)
        self.ui.chromatogram2.canvas.ax.clear()
        self.ui.chromatogram2.canvas.draw()
        self.ui.chromatogram2.setEnabled(False)
        self.ui.mass_spectrum.canvas.ax.clear()
        self.ui.mass_spectrum.canvas.draw()
        self.ui.mass_spectrum.setEnabled(False)
        self.ui.electron_image.canvas.ax.clear()
        self.ui.electron_image.canvas.draw()
        self.ui.electron_image.setEnabled(False)

    # When the chromatogram is double-clicked, the event below will execute
    def on_click(self, event):
        if event.dblclick:
            try:
                ix = round(float(event.xdata), 2)  # Location of the plot click
                index = np.where(self.test_file_time == ix)[0][0]  # Index location on where the line_x should appear
                line_x = self.test_file_time[index]
                self.ui.chromatogram1.canvas.ax.clear()
                self.ui.chromatogram2.canvas.ax.clear()
                self.ui.chromatogram1.canvas.ax.plot(self.test_file_time, self.test_file_Ch1_FF_intensity)
                self.ui.chromatogram2.canvas.ax.plot(self.test_file_time, self.test_file_Ch2_FF_intensity)
                self.ui.chromatogram1.canvas.ax.plot([line_x, line_x], [min(self.test_file_Ch1_FF_intensity), max(self.test_file_Ch1_FF_intensity)])
                self.ui.chromatogram2.canvas.ax.plot([line_x, line_x], [min(self.test_file_Ch2_FF_intensity), max(self.test_file_Ch2_FF_intensity)])
                self.ui.chromatogram1.canvas.draw()
                self.ui.chromatogram2.canvas.draw()
                self.ui.mass_spectrum.canvas.ax.clear()

                # Selecting the TOF file based on which location of the plot has been clicked
                with h5py.File('Files/scan_example.h5', 'r') as f:
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
                with h5py.File('Files/example.h5', 'r') as f:
                    picture_nr = round(abs(round(ix)) / max(self.test_file_time) * 9)
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

    # The function to open the chiral MS window
    def open_chiral_ms_window(self):
        self.window_MS = ChiralMsController()

    def open_file(self):
        self.MainWindow.close()
        self.fileBrowserWidget = file_browser.FileBrowserController(open_file=True, main=True)
        self.fileBrowserWidget.show()
        self.fileBrowserWidget.set_path()

#
# # The hard workers, also known as the threads
# class Worker1(QObject):
#     finished1 = pyqtSignal()
#     progress1 = pyqtSignal(int)
#
#     def run(self):
#         while v.check1 is True:
#             tb = time()
#             self.progress1.emit(v.i1 + 1)
#             te = time()
#             sleep(1 - (te - tb))  # Getting a more accurate sleep(1)
#         self.finished1.emit()
#
#
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
