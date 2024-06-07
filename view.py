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

        self.plot_widget = pg.PlotWidget()
        self.plot_widget.setTitle("Real-time Data")
        self.plot_widget.setLabel('left', 'Value')
        self.plot_widget.setLabel('bottom', 'Time', 's')
        self.plot_widget.showGrid(x=True, y=True)
        self.right_layout.addWidget(self.plot_widget)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)
