from sys import argv, exit
from time import time, sleep

import numpy as np
from PyQt5 import QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtGui import QPixmap

import values as v
from chiral_ms_controller import chiral_ms_controller
from injector_controller import Injector_controller
from mass_spectrum_window import Ui_zoom_in_mass_spectrum
from micro_gc_controller import micro_GC_controller
from real_gui import Ui_MainWindow


class Controller:
    def __init__(self) -> object:
        app = QtWidgets.QApplication(argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.MainWindow.show()

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

        # Executing the application
        exit(app.exec_())

    # start the data acquisition
    def start(self):
        self.ui.chromatogram.canvas.ax.plot(v.test_file_x, v.test_file_y)
        self.ui.chromatogram.canvas.draw()
        self.ui.start_button.setEnabled(False)
        self.ui.stop_button.setEnabled(True)

        # Showing an electron image in a QGraphicsView
        pix = QPixmap('electron_image.png')
        item = QtWidgets.QGraphicsPixmapItem(pix)
        scene = QtWidgets.QGraphicsScene()
        scene.addItem(item)
        self.ui.electron_image.setScene(scene)

    # Stop the data acquisition
    def stop(self):
        self.ui.start_button.setEnabled(True)
        self.ui.stop_button.setEnabled(False)
        self.ui.chromatogram.canvas.ax.clear()
        self.ui.chromatogram.canvas.draw()

        # clearing the electron image
        self.ui.electron_image.scene().clear()

    def on_click(self, event):
        if event.dblclick:
            # Opening the mass spectrum window
            self.window_mass_spectrum = QtWidgets.QMainWindow()
            self.ui_mass = Ui_zoom_in_mass_spectrum()
            self.ui_mass.setupUi(self.window_mass_spectrum)
            self.window_mass_spectrum.show()

            # Defining the data around the double click event location
            ix = round(float(event.xdata), 2)
            index = np.where(v.test_file_x == ix)[0][0]
            fragment = round(v.length * 0.025)
            plot_x = v.test_file_x[(index - fragment):(index + fragment)]
            plot_y = v.test_file_y[(index - fragment):(index + fragment)]
            self.ui_mass.mass_spectrum.canvas.ax.plot(plot_x, plot_y)
            self.ui_mass.mass_spectrum.canvas.draw()

            # # Making a line where the double click occurred
            # line_x = v.test_file_x[index]
            # self.ui.chromatogram.canvas.ax.plot([line_x, line_x], [-2.5, 13])
            # self.ui.chromatogram.canvas.draw()

    # The function to open the injector window
    def open_injector_window(self):
        self.window_in = Injector_controller()

    # The function to open the micro GC window
    def open_micro_gc_window(self):
        self.window_GC = micro_GC_controller()

    # The function to open the chiral MS window
    def open_chiral_ms_window(self):
        self.window_MS = chiral_ms_controller()

    # def chromatogram(self):
    #     v.row_x1 = v.row_x1 + 1
    #     v.x1 = append(v.x1, v.row_x1)
    #     v.y1 = append(v.y1, v.y1[-1] + randint(-1, 1))
    #     self.ui.chromatogram.addItem(PlotDataItem(v.x1, v.y1))
    #
    #     # Max length of the graph will be no longer than 100 seconds long
    #     if len(v.x1) > 100:
    #         self.ui.chromatogram.plotItem.setLimits(xMin=len(v.x1) - 100, xMax=len(v.x1))

    # The thread that will run a process parallel to the main process
    # def chromatogram_worker(self):
    #     self.thread1 = QThread()
    #     self.worker1 = Worker1()
    #     self.worker1.moveToThread(self.thread1)
    #     self.thread1.started.connect(self.worker1.run)
    #     self.worker1.finished1.connect(self.thread1.quit)
    #     self.worker1.finished1.connect(self.worker1.deleteLater)
    #     self.thread1.finished.connect(self.thread1.deleteLater)
    #     self.worker1.progress1.connect(self.chromatogram)
    #     self.thread1.start()
    #     self.ui.start_button.setEnabled(False)
    #     self.ui.stop_button.setEnabled(True)
    #     self.thread1.finished.connect(lambda: self.ui.start_button.setEnabled(True))
    #
    # def stop_chromatogram_worker(self):
    #     v.check1 = False
    #     self.ui.stop_button.setEnabled(False)
    #     self.ui.start_button.setEnabled(True)
    #     sleep(1)
    #     v.check1 = True


# The hard workers, also known as the threads
class Worker1(QObject):
    finished1 = pyqtSignal()
    progress1 = pyqtSignal(int)

    def run(self):
        while v.check1 is True:
            tb = time()
            self.progress1.emit(v.i1 + 1)
            te = time()
            sleep(1 - (te - tb))  # Getting a more accurate sleep(1)
        self.finished1.emit()


class Worker2(QObject):
    finished2 = pyqtSignal()
    progress2 = pyqtSignal(int)

    def run(self):
        while v.check2 is True:
            tb = time()
            sleep(1)
            te = time()
            sleep(1 - (te - tb))  # Getting a more accurate than sleep(1)
            self.progress2.emit(v.i2 + 1)
        self.finished2.emit()
