import json
import hvc_controller

from os import getcwd
from PyQt5 import QtCore, QtWidgets

import microGC_controller


class FileBrowserController(QtWidgets.QMainWindow):
    def __init__(self, save_file=False, open_file=False, microGC=False, hvc=False,  hvc_data=None, microGC_data=None):
        QtWidgets.QMainWindow.__init__(self)
        self.window_hvc = None
        self.open_filename = None
        self.filename = None
        self.window_GC = None
        self.setGeometry(560, 240, 600, 600)
        self.fileBrowserWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.fileBrowserWidget)
        self.dir_model = QtWidgets.QFileSystemModel()

        # The frames inside the fileBrowserWidget
        self.frame_1 = QtWidgets.QFrame(self.fileBrowserWidget)
        self.frame_1.setGeometry(20, 20, 560, 510)
        self.frame_2 = QtWidgets.QFrame(self.fileBrowserWidget)
        self.frame_2.setGeometry(20, 550, 560, 30)

        # The lineEdit inside frame_2
        self.file_line = QtWidgets.QLineEdit(self.frame_2)
        self.file_line.setGeometry(QtCore.QRect(9, 5, 440, 20))
        self.save_cancel = QtWidgets.QDialogButtonBox(self.frame_2)

        # Defining the buttons for when save or open is used
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

        box = QtWidgets.QHBoxLayout(self.frame_1)
        box.addWidget(splitter_filebrowser)

        # Defining the data that is being supplied
        self.hvc_data = hvc_data
        self.microGC_data = microGC_data

        # The file browser will execute if certain conditions are met
        if save_file and hvc:
            self.save_cancel.accepted.connect(self.save_hvc)

        if save_file and microGC:
            self.save_cancel.accepted.connect(self.save_microGC)

        if open_file and hvc:
            self.save_cancel.accepted.connect(self.open_hvc)

        if open_file and microGC:
            self.save_cancel.accepted.connect(self.open_microGC)

        self.save_cancel.rejected.connect(self.close)

    def set_path(self):
        self.dir_model.setRootPath("")  # This will set the directory to all, if called upon

    def clicked(self):
        # Get selected path of folder_view
        index = self.selectionModel.currentIndex()
        dir_path = self.dir_model.filePath(index)
        self.file_model.setRootPath(dir_path)
        self.file_view.setRootIndex(self.file_model.index(dir_path))

    def file(self):
        index = self.file_view.currentIndex()
        self.filename = self.file_model.fileName(index)
        if self.filename[-5:] == '.json':
            self.file_line.setText(self.filename[:len(self.filename)-5])
        else:
            self.file_line.setText(self.filename)

    def save_hvc(self):  # This function will save the hvc settings in a json file
        save_filename = self.file_line.text()
        with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + save_filename + '.json', 'w') as f:
            json.dump(self.hvc_data, f)
        print(f'{save_filename} is saved at {getcwd()}/Chiral MS settings/High Voltage Control')
        self.close()

    def open_hvc(self):  # This function will open the hvc settings of a json file
        open_filename = self.file_line.text()
        try:
            with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + open_filename + '.json', 'r') as f:
                hvc_settings = json.load(f)
                self.window_hvc = hvc_controller.HvcController(file=True, data=hvc_settings)
                print(f'File {open_filename} is opened')
        except Exception as e:
            print(f'{e}')
        self.close()

    def save_microGC(self):
        save_filename = self.file_line.text()
        with open(getcwd() + '/Chiral MS settings/MicroGC/' + save_filename + '.json', 'w') as f:
            json.dump(self.microGC_data, f)
        print(f'{save_filename} is saved at {getcwd}/Chiral Ms settings/MicroGC')
        self.close()

    def open_microGC(self):
        open_filename = self.file_line.text()
        try:
            with open(getcwd() + '/Chiral MS settings/MicroGC/' + open_filename + '.json', 'r') as f:
                microGC_settings = json.load(f)
                self.window_GC = microGC_controller.MicroGcController(file=True, data=microGC_settings)
                print(f'File {open_filename} is opened')
        except Exception as e:
            print(f'{e}')
        self.close()
