import json
import hvc_controller

from os import getcwd
from PyQt5 import QtCore, QtWidgets


class FileBrowserController(QtWidgets.QMainWindow):
    def __init__(self, save_file=False, open_file=False, microGC=False, hvc=False,  hvc_data=None):
        QtWidgets.QMainWindow.__init__(self)
        self.open_filename = None
        self.filename = None
        self.setGeometry(560, 240, 600, 600)
        self.fileBrowserWidget = QtWidgets.QWidget(self)
        self.setCentralWidget(self.fileBrowserWidget)
        self.dirmodel = QtWidgets.QFileSystemModel()

        # The frames inside the fileBrowserWidget
        self.frame_1 = QtWidgets.QFrame(self.fileBrowserWidget)
        self.frame_1.setGeometry(20, 20, 560, 510)
        self.frame_2 = QtWidgets.QFrame(self.fileBrowserWidget)
        self.frame_2.setGeometry(20, 550, 560, 30)

        # The lineEdit inside frame_2
        self.file_line = QtWidgets.QLineEdit(self.frame_2)
        self.file_line.setGeometry(QtCore.QRect(9, 5, 440, 20))
        self.save_cancel = QtWidgets.QDialogButtonBox(self.frame_2)

        if save_file:
            self.save_cancel.setStandardButtons((QtWidgets.QDialogButtonBox.Save | QtWidgets.QDialogButtonBox.Cancel))
        if open_file:
            self.save_cancel.setStandardButtons((QtWidgets.QDialogButtonBox.Open | QtWidgets.QDialogButtonBox.Cancel))
        self.save_cancel.setGeometry(460, 0, 90, 30)

        # Don't show files, just folders
        self.dirmodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs)
        self.folder_view = QtWidgets.QTreeView()
        self.folder_view.setModel(self.dirmodel)
        self.folder_view.clicked[QtCore.QModelIndex].connect(self.clicked)

        # Don't show columns for size, file type, and last modified
        self.folder_view.setHeaderHidden(True)
        self.folder_view.hideColumn(1)
        self.folder_view.hideColumn(2)
        self.folder_view.hideColumn(3)

        self.selectionModel = self.folder_view.selectionModel()
        self.filemodel = QtWidgets.QFileSystemModel()

        # Don't show folders, just files
        self.filemodel.setFilter(QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Files)
        self.file_view = QtWidgets.QListView()
        self.file_view.setModel(self.filemodel)
        self.file_view.clicked[QtCore.QModelIndex].connect(self.file)

        splitter_filebrowser = QtWidgets.QSplitter()
        splitter_filebrowser.addWidget(self.folder_view)
        splitter_filebrowser.addWidget(self.file_view)
        splitter_filebrowser.setStretchFactor(0, 2)
        splitter_filebrowser.setStretchFactor(1, 4)

        hbox = QtWidgets.QHBoxLayout(self.frame_1)
        hbox.addWidget(splitter_filebrowser)

        self.data = hvc_data

        if save_file and hvc:
            self.save_cancel.accepted.connect(self.save_hvc)

        if save_file and microGC:
            self.save_cancel.accepted.connect(self.save_other)

        if open_file and microGC:
            self.save_cancel.accepted.connect(self.open_other)

        if open_file and hvc:
            self.save_cancel.accepted.connect(self.open_hvc)

        self.save_cancel.rejected.connect(self.close)

    def set_path(self):
        self.dirmodel.setRootPath("")  # This will set the directory to all, if called upon

    def clicked(self):
        # get selected path of folder_view
        index = self.selectionModel.currentIndex()
        dir_path = self.dirmodel.filePath(index)
        self.filemodel.setRootPath(dir_path)
        self.file_view.setRootIndex(self.filemodel.index(dir_path))

    def file(self):
        index = self.file_view.currentIndex()
        self.filename = self.filemodel.fileName(index)
        self.file_line.setText(self.filename)

    def save_hvc(self):  # This function will save the hvc settings in a json file
        filename = self.file_line.text()
        with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + filename + '.json', 'w') as f:
            json.dump(self.data, f)
        print(f'{filename} is saved at {getcwd()}/Chiral MS settings/High Voltage Control')
        self.close()

    def open_hvc(self):  # This function will open the hvc settings of a json file
        open_filename = self.file_line.text()
        try:
            with open(getcwd() + '/Chiral MS settings/High Voltage Control/' + open_filename + '.json', 'r') as f:
                hvc_settings = json.load(f)
                self.window_hvc = hvc_controller.OpenHvcController(file=True, data=hvc_settings)
                print(f'File {open_filename} is opened')
        except:
            print('File not found')

        self.close()

    def save_other(self):  # TODO: Make this function actually save the settings
        filename = self.file_line.text()
        print(f'{filename} is saved')
        self.close()

    def open_other(self):  # TODO: Make this function actually open the settings
        open_filename = self.file_line.text()
        print(f'File {open_filename} is opened')
        self.close()
