from PyQt5 import QtWidgets
from microGC_settings import Ui_microGC_settings
from file_browser import FileBrowserController


class micro_GC_controller:
    def __init__(self) -> object:
        self.window_GC = QtWidgets.QMainWindow()
        self.ui_GC = Ui_microGC_settings()
        self.ui_GC.setupUi(self.window_GC)
        self.window_GC.show()

        # The settings for the plot
        self.ui_GC.temperature_trajectory.canvas.fig.text(0.82, 0.16, '(min)', ha='center', va='center')
        self.ui_GC.temperature_trajectory.canvas.fig.text(0.02, 0.5, 'Temperature (°C)', ha='center', va='center', rotation='vertical')
        self.ui_GC.temperature_trajectory.canvas.ax.grid()

        def open_file_browser():
            self.fileBrowserWidget = FileBrowserController()
            self.fileBrowserWidget.show()
            # # The command below will enable the entire directory in the open_file_browser menu
            # self.fileBrowserWidget.set_path()

        def update_graph():
            try:
                # Clear the previous data
                self.ui_GC.temperature_trajectory.canvas.ax.clear()
                self.ui_GC.temperature_trajectory.canvas.ax.grid()

                # The initial temperature and time
                temperature_trajectory = [float(self.ui_GC.temperature_table.item(0, 1).text())]
                time_trajectory = [0]

                # The plot data for the range of the table
                for i in range(1, self.ui_GC.temperature_table.rowCount()):
                    temperature_trajectory.append(float(self.ui_GC.temperature_table.item(i, 1).text()))
                    time_end = time_trajectory[-1] + (abs(temperature_trajectory[-1] - temperature_trajectory[-2]) /
                                                      float(self.ui_GC.temperature_table.item(i, 0).text()))
                    time_trajectory.append(time_end)

                    # When hold time is > 0 then append another data point
                    if float(self.ui_GC.temperature_table.item(i, 2).text()) > 0:
                        temperature_trajectory.append(float(self.ui_GC.temperature_table.item(i, 1).text()))
                        time_trajectory.append(time_trajectory[-1] + float(self.ui_GC.temperature_table.item(i, 2).text()))

                # Plot the data
                self.ui_GC.temperature_trajectory.canvas.ax.plot(time_trajectory, temperature_trajectory)
                self.ui_GC.temperature_trajectory.canvas.draw()

                # Updating the total time label
                self.ui_GC.total_time.setText(str(round(time_trajectory[-1], 2)))

            except:
                print('All fields must contain data')

        def add_row():
            self.ui_GC.temperature_table.insertRow(self.ui_GC.temperature_table.rowCount())

        def remove_row():
            self.ui_GC.temperature_table.removeRow(self.ui_GC.temperature_table.rowCount() - 1)

        # The buttons and their function
        self.ui_GC.set_graph.clicked.connect(update_graph)
        self.ui_GC.add_row.clicked.connect(add_row)
        self.ui_GC.remove_row.clicked.connect(remove_row)

        # Drop down menu and their functions
        self.ui_GC.action_Open.triggered.connect(open_file_browser)
        self.ui_GC.action_Save_as.triggered.connect(open_file_browser)
