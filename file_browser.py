import json
import numpy as np
from PyQt5.QtCore import QDir

import hvc_controller
import main_gui_controller
import microGC_controller

from os import getcwd
from PyQt5 import QtCore, QtWidgets


class FileBrowserController(QtWidgets.QMainWindow):
    def __init__(self, save_file=False, open_file=False, microGC=False, hvc=False, main=False, hvc_data=None, microGC_data=None):
        QtWidgets.QMainWindow.__init__(self)
        self.index = None
        self.dir_path = None
        self.filename = None
        self.window_GC = None
        self.window_hvc = None
        self.MainWindow = None
        self.open_filename = None

        self.setGeometry(560, 240, 600, 600)
        self.fileBrowserWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.fileBrowserWidget)
        self.dir_model = QtWidgets.QFileSystemModel()

        # The frames inside the fileBrowserWidget
        self.frame1 = QtWidgets.QFrame(self.fileBrowserWidget)
        self.frame1.setGeometry(20, 20, 560, 510)
        self.frame2 = QtWidgets.QFrame(self.fileBrowserWidget)
        self.frame2.setGeometry(20, 550, 560, 30)

        # The lineEdit inside frame_2
        self.file_line = QtWidgets.QLineEdit(self.frame2)
        self.file_line.setGeometry(QtCore.QRect(9, 5, 440, 20))
        self.save_cancel = QtWidgets.QDialogButtonBox(self.frame2)

        # Defining the buttons for when save or open is called upon
        if save_file:
            self.save_cancel.setStandardButtons((QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel))
        if open_file:
            self.save_cancel.setStandardButtons((QtWidgets.QDialogButtonBox.Open | QtWidgets.QDialogButtonBox.Cancel))
        self.save_cancel.setGeometry(460, 0, 90, 30)

        # Don't show files, just folders
        self.dir_model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
        self.folder_view = QtWidgets.QTreeView()
        self.folder_view.setModel(self.dir_model)
        self.folder_view.clicked[QtCore.QModelIndex].connect(self.clicked)

        # Don't show columns for size, file type, and last modified
        self.folder_view.setHeaderHidden(True)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)

        self.selectionModel = self.folder_view.selectionModel()
        self.file_model = QtWidgets.QFileSystemModel()

        # Don't show folders, just files
        self.file_model.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.file_view = QtWidgets.QListView()
        self.file_view.setModel(self.file_model)
        self.file_view.clicked[QtCore.QModelIndex].connect(self.file)

        # The feature for splitting the file browser into two
        splitter_filebrowser = QtWidgets.QSplitter()
        splitter_filebrowser.addWidget(self.folder_view)
        splitter_filebrowser.addWidget(self.file_view)
        splitter_filebrowser.setStretchFactor(0, 2)
        splitter_filebrowser.setStretchFactor(1, 4)

        box = QtWidgets.QHBoxLayout(self.frame1)
        box.addWidget(splitter_filebrowser)

        # Defining the data that is being called upon with
        self.hvc_data = hvc_data
        self.microGC_data = microGC_data

        # The file browser will execute if certain conditions are met
        if save_file and hvc:
            self.save_cancel.accepted.connect(self.save_hvc)
            self.file_model.setNameFilters(["*.json"])

        if open_file and hvc:
            self.save_cancel.accepted.connect(self.open_hvc)
            self.file_model.setNameFilters(["*.json"])

        if save_file and microGC:
            self.save_cancel.accepted.connect(self.save_microGC)
            self.file_model.setNameFilters(["*.json"])

        if open_file and microGC:
            self.save_cancel.accepted.connect(self.open_microGC)
            self.file_model.setNameFilters(["*.json"])

        if open_file and main:
            self.save_cancel.accepted.connect(self.load_data)
            self.file_model.setNameFilters(["*.txt"])

        self.save_cancel.rejected.connect(self.close)

    # This will set the directory to all, if called upon
    def set_path(self):
        self.dir_model.setRootPath('')

    # Get selected path of folder_view
    def clicked(self):
        self.index = self.selectionModel.currentIndex()
        self.dir_path = self.dir_model.filePath(self.index)
        self.file_model.setRootPath(self.dir_path)
        self.file_view.setRootIndex(self.file_model.index(self.dir_path))

    # Put the selected file in the line edit, but filter out .json
    def file(self):
        index = self.file_view.currentIndex()
        self.filename = self.file_model.fileName(index)
        self.file_line.setText(self.filename)

    # This function will save the hvc settings in a json file
    def save_hvc(self):
        save_filename = self.file_line.text()
        with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + save_filename + '.json', 'w') as f:
            json.dump(self.hvc_data, f)
        print(f'{save_filename} is saved at {str(getcwd())}\\Chiral MS settings\\High Voltage Control')
        self.close()

    # This function will open the hvc settings of a json file
    def open_hvc(self):
        open_filename = self.file_line.text()
        try:
            with open(self.dir_path + '/' + open_filename, 'r') as f:
                hvc_settings = json.load(f)
                self.window_hvc = hvc_controller.HvcController(file=True, data=hvc_settings)
                print(f'File {open_filename} is opened')
        except Exception as e:
            print(e)
        self.close()

    # This function will save the microGC settings in a json file
    def save_microGC(self):
        save_filename = self.file_line.text()
        with open(getcwd() + '/Chiral MS settings/MicroGC/' + save_filename + '.json', 'w') as f:
            json.dump(self.microGC_data, f)
        print(f'{save_filename} is saved at {str(getcwd())}\\Chiral MS settings\\MicroGC')
        self.close()

    # This function will open the microGC settings of a json file
    def open_microGC(self):
        open_filename = self.file_line.text()
        try:
            with open(self.dir_path + '/' + open_filename, 'r') as f:
                microGC_settings = json.load(f)
                self.window_GC = microGC_controller.MicroGcController(file=True, data=microGC_settings)
                print(f'File {open_filename} is opened')
        except Exception as e:
            print(e)
        self.close()

    # This function will open the main window with a selected file
    def load_data(self):
        open_filename = self.dir_path + '/' + self.file_line.text()
        try:
            file = open_filename
            test_file_time = np.loadtxt(file, skiprows=3, usecols=0)
            Ch1_FF = np.loadtxt(file, skiprows=3, usecols=1)
            Ch2_FF = np.loadtxt(file, skiprows=3, usecols=2)
            Ch3_BF = np.loadtxt(file, skiprows=3, usecols=3)
            data = [test_file_time, Ch1_FF, Ch2_FF, Ch3_BF]
            self.MainWindow = main_gui_controller.Controller(load=True, data=data)
        except Exception as e:
            print(e)
        self.close()
