import h5py
import numpy as np
import values as v

# from time import time, sleep
from sys import argv, exit
from PyQt5 import QtWidgets
# from PyQt5.QtCore import QObject, pyqtSignal
from chiralMS_controller import ChiralMsController
from injector_controller import Injector_controller
from microGC_controller import MicroGcController
from real_gui import Ui_MainWindow


class Controller:
    def __init__(self):
        self.window_in = None
        self.window_GC = None
        self.window_MS = None
        app = QtWidgets.QApplication(argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

        # Maximizing the screen
        self.MainWindow.showMaximized()

        # Disabling the plots
        self.ui.chromatogram.setEnabled(False)
        self.ui.mass_spectrum.setEnabled(False)
        self.ui.electron_image.setEnabled(False)

        # The buttons and their functions
        self.ui.injector_settings_button.clicked.connect(self.open_injector_window)
        self.ui.microGC_settings_button.clicked.connect(self.open_micro_gc_window)
        self.ui.chiralMS_settings_button.clicked.connect(self.open_chiral_ms_window)

        # # The start and stop button
        self.ui.start_button.clicked.connect(self.start)
        self.ui.stop_button.clicked.connect(self.stop)

        # The chromatogram settings
        self.ui.chromatogram.canvas.mpl_connect('button_press_event', self.on_click)
        self.ui.chromatogram.canvas.fig.text(0.85, 0.15, 'Retention time (min)', ha='center', va='center')
        self.ui.chromatogram.canvas.fig.text(0.09, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')
        self.ui.mass_spectrum.canvas.fig.text(0.85, 0.05, 'Index nr.', ha='center', va='center')
        self.ui.mass_spectrum.canvas.fig.text(0.05, 0.5, 'Intensity', ha='center', va='center', rotation='vertical')

        # Executing the application
        exit(app.exec_())

    # Start the data acquisition
    def start(self):
        # Disabling and enabling the stop and start buttons
        self.ui.start_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)
        self.ui.chromatogram.setEnabled(True)
        self.ui.mass_spectrum.setEnabled(True)
        self.ui.electron_image.setEnabled(True)

        # Plotting the chromatogram
        self.ui.chromatogram.canvas.ax.clear()
        self.ui.chromatogram.canvas.ax.plot(v.test_file_x, v.test_file_y)
        self.ui.chromatogram.canvas.draw()

    # Stop the data acquisition
    def stop(self):
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        self.ui.chromatogram.canvas.ax.clear()
        self.ui.chromatogram.canvas.draw()
        self.ui.chromatogram.setEnabled(False)
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
                ix = round(float(event.xdata))  # Location of the plot click
                index = np.where(v.test_file_x == ix)[0][0]  # Index location on where the line_x should appear
                line_x = v.test_file_x[index]
                self.ui.chromatogram.canvas.ax.clear()
                self.ui.chromatogram.canvas.ax.plot(v.test_file_x, v.test_file_y)
                self.ui.chromatogram.canvas.ax.plot([line_x, line_x], [min(v.test_file_y), max(v.test_file_y)])
                self.ui.chromatogram.canvas.draw()

                self.ui.mass_spectrum.canvas.ax.clear()
                with h5py.File('Files/scan_example.h5', 'r') as f:
                    tof_list = list(f.keys())[0]

                    # Creating a list for the files in TOF
                    x = []
                    for _ in f[tof_list]:
                        x.append(_)

                    # Selecting the TOF file based on what location of the plot has been clicked
                    tof_nr = f[tof_list][x[abs(ix)]]
                    tof = np.squeeze(tof_nr['TOF0'])
                    self.ui.mass_spectrum.canvas.ax.plot(tof)
                    self.ui.mass_spectrum.canvas.draw()

                with h5py.File('Files/example.h5', 'r') as f:
                    picture_nr = round(abs(ix) / max(v.test_file_x) * 9)
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
