from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, \
    QSlider, QLineEdit, QLabel, QComboBox, QGroupBox, QTabWidget, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot

class SliderWithText(QWidget):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.label = QLabel(label_text)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.text = QLineEdit()
        self.text.setFixedWidth(50)

        self.min_label = QLabel("Min:")
        self.min_text = QLineEdit()
        self.min_text.setFixedWidth(50)
        self.min_text.setText("0")

        self.max_label = QLabel("Max:")
        self.max_text = QLineEdit()
        self.max_text.setFixedWidth(50)
        self.max_text.setText("100")

        self.text_layout = QHBoxLayout()
        self.text_layout.addWidget(self.label)
        self.text_layout.addWidget(self.text)

        self.slider_layout = QHBoxLayout()
        self.slider_layout.addWidget(self.slider)

        self.range_layout = QHBoxLayout()
        self.range_layout.addWidget(self.min_label)
        self.range_layout.addWidget(self.min_text)
        self.range_layout.addStretch()  # Add stretch to push max elements to the right
        self.range_layout.addWidget(self.max_text)
        self.range_layout.addWidget(self.max_label)

        self.layout.addLayout(self.text_layout)
        self.layout.addLayout(self.slider_layout)
        self.layout.addLayout(self.range_layout)

        self.setLayout(self.layout)

        self.slider.valueChanged.connect(self.update_text)
        self.text.textChanged.connect(self.update_slider)
        self.min_text.editingFinished.connect(self.update_min)
        self.max_text.editingFinished.connect(self.update_max)

    @pyqtSlot(int)
    def update_text(self, value):
        self.text.setText(str(value))

    @pyqtSlot()
    def update_slider(self):
        try:
            value = int(self.text.text())
            if self.slider.minimum() <= value <= self.slider.maximum():
                self.slider.setValue(value)
        except ValueError:
            pass  # Ignore invalid input

    @pyqtSlot()
    def update_min(self):
        try:
            min_value = int(self.min_text.text())
            max_value = self.slider.maximum()
            self.slider.setRange(min_value, max_value)
            self.update_slider()  # Update the slider value to ensure it's within the new range
        except ValueError:
            pass  # Ignore invalid input

    @pyqtSlot()
    def update_max(self):
        try:
            max_value = int(self.max_text.text())
            min_value = self.slider.minimum()
            self.slider.setRange(min_value, max_value)
            self.update_slider()  # Update the slider value to ensure it's within the new range
        except ValueError:
            pass  # Ignore invalid input

class LEDIndicator(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(20, 20)
        self.setStyleSheet("background-color: red; border-radius: 10px;")

    def set_on(self):
        self.setStyleSheet("background-color: green; border-radius: 10px;")

    def set_off(self):
        self.setStyleSheet("background-color: red; border-radius: 10px;")

class OutputWidget(QWidget):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)

        self.layout = QVBoxLayout()

        self.label = QLabel(label_text)
        self.output = QTextEdit()
        self.output.setReadOnly(True)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.output)

        self.setLayout(self.layout)