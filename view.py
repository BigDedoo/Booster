from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QListWidget, QVBoxLayout, QWidget


class DeviceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port and NI Devices")

        self.layout = QVBoxLayout()

        self.refresh_button = QPushButton("Refresh")
        self.device_list = QListWidget()

        self.layout.addWidget(self.refresh_button)
        self.layout.addWidget(self.device_list)

        container = QWidget()
        container.setLayout(self.layout)
        self.setCentralWidget(container)
