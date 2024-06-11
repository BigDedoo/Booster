from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout
import pyqtgraph as pg

class DeviceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port and NI Devices")

        self.main_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.device_list = QListWidget()
        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.stop_button = QPushButton("Stop")

        self.left_layout.addWidget(self.refresh_button)
        self.left_layout.addWidget(self.device_list)
        self.left_layout.addWidget(self.data_display)
        self.left_layout.addWidget(self.stop_button)

        self.plot_widget_1 = pg.PlotWidget()
        self.plot_widget_1.setTitle("Real-time Data - Plot 1")
        self.plot_widget_1.setLabel('left', 'Value')
        self.plot_widget_1.setLabel('bottom', 'Time', 's')
        self.plot_widget_1.showGrid(x=True, y=True)

        self.plot_widget_2 = pg.PlotWidget()
        self.plot_widget_2.setTitle("Real-time Data - Plot 2")
        self.plot_widget_2.setLabel('left', 'Value')
        self.plot_widget_2.setLabel('bottom', 'Time', 's')
        self.plot_widget_2.showGrid(x=True, y=True)

        self.right_layout.addWidget(self.plot_widget_1)
        self.right_layout.addWidget(self.plot_widget_2)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
