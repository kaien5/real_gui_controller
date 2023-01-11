import h5py
from PyQt5 import QtWidgets
from electron_image import Ui_electron_image_window


class ElectronImageController:
    def __init__(self, data, ix):
        self.fileBrowserWidget = None
        self.electron_image = QtWidgets.QMainWindow()
        self.ui_EC = Ui_electron_image_window()
        self.ui_EC.setupUi(self.electron_image)
        self.electron_image.show()

        with h5py.File('Data/example.h5', 'r') as f:
            picture_nr = round(abs(round(ix)) / max(data) * 9)
            electron_list = list(f.keys())[0]
            electron_images = f[electron_list][()]
            self.ui_EC.electron_image.canvas.ax.imshow(electron_images[picture_nr])
            self.ui_EC.electron_image.canvas.ax.axis('off')
            self.ui_EC.electron_image.canvas.ax.set_title('Electron image')
            self.ui_EC.electron_image.canvas.draw()
