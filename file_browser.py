import sys
from PyQt5 import QtCore, QtWidgets


class FileBrowserController(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
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
        self.save_cancel.setStandardButtons((QtWidgets.QDialogButtonBox.Save|QtWidgets.QDialogButtonBox.Cancel))
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

        splitter_filebrowser = QtWidgets.QSplitter()
        splitter_filebrowser.addWidget(self.folder_view)
        splitter_filebrowser.addWidget(self.file_view)
        splitter_filebrowser.setStretchFactor(0, 2)
        splitter_filebrowser.setStretchFactor(1, 4)

        hbox = QtWidgets.QHBoxLayout(self.frame_1)
        hbox.addWidget(splitter_filebrowser)

        self.save_cancel.accepted.connect(self.save_button)
        self.save_cancel.rejected.connect(self.cancel_button)

    def set_path(self):
        self.dirmodel.setRootPath("")

    def clicked(self, index):
        # get selected path of folder_view
        index = self.selectionModel.currentIndex()
        dir_path = self.dirmodel.filePath(index)
        print(dir_path)
        self.filemodel.setRootPath(dir_path)
        self.file_view.setRootIndex(self.filemodel.index(dir_path))

    def save_button(self):
        filename = self.file_line.text()
        print(filename)

    def cancel_button(self):
        self.fileBrowserWidget.close()
