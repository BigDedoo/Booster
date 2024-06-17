from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, \
    QSlider, QLineEdit, QLabel, QComboBox, QGroupBox
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
import pyqtgraph as pg


class LEDIndicator(QLabel):
    def __init__(self):
        super().__init__()
        self.setFixedSize(20, 20)
        self.setStyleSheet("background-color: red; border-radius: 10px;")

    def set_on(self):
        self.setStyleSheet("background-color: green; border-radius: 10px;")

    def set_off(self):
        self.setStyleSheet("background-color: red; border-radius: 10px;")


class SliderWithText(QWidget):
    def __init__(self, label_text, parent=None):
        super().__init__(parent)

        self.layout = QHBoxLayout()

        self.label = QLabel(label_text)
        self.slider = QSlider(Qt.Orientation.Horizontal)
        self.slider.setRange(0, 100)
        self.slider.setValue(50)
        self.text = QLineEdit()
        self.text.setFixedWidth(50)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slider)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)

        self.slider.valueChanged.connect(self.update_text)
        self.text.textChanged.connect(self.update_slider)

    @pyqtSlot(int)
    def update_text(self, value):
        self.text.setText(str(value))

    @pyqtSlot()
    def update_slider(self):
        try:
            value = int(self.text.text())
            if 0 <= value <= 100:
                self.slider.setValue(value)
        except ValueError:
            pass  # Ignore invalid input


class DeviceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port and NI Devices")

        self.main_layout = QHBoxLayout()

        self.left_layout = QVBoxLayout()
        self.right_layout = QVBoxLayout()

        self.data_display = QTextEdit()
        self.data_display.setReadOnly(True)
        self.stop_button = QPushButton("Stop")

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

        self.left_layout.addWidget(self.plot_widget_1)
        self.left_layout.addWidget(self.plot_widget_2)

        # Create a horizontal layout for "Source Cathode", "Einzel Extraction", and the new section
        self.horizontal_layout = QHBoxLayout()

        # Add new section for "source cathode" in a group box
        self.source_cathode_group = QGroupBox("Source Cathode")
        self.source_cathode_layout = QVBoxLayout()

        self.slider1 = SliderWithText("Slider 1")
        self.slider2 = SliderWithText("Slider 2")
        self.input_label = QLabel("Input Text")
        self.input_text = QLineEdit()

        self.source_cathode_layout.addWidget(self.slider1)
        self.source_cathode_layout.addWidget(self.slider2)
        self.source_cathode_layout.addWidget(self.input_label)
        self.source_cathode_layout.addWidget(self.input_text)
        self.source_cathode_group.setLayout(self.source_cathode_layout)

        # Add new section for "Einzel extraction" in a group box
        self.einzel_group = QGroupBox("Einzel Extraction")
        self.einzel_layout = QVBoxLayout()

        self.einzel_slider1 = SliderWithText("Einzel Slider 1")
        self.einzel_slider2 = SliderWithText("Einzel Slider 2")
        self.einzel_input_labels = [QLabel(f"Einzel Input {i + 1}") for i in range(2)]
        self.einzel_inputs = [QLineEdit() for _ in range(2)]

        self.einzel_output_label = QLabel("Einzel Output")
        self.einzel_output = QTextEdit()
        self.einzel_output.setReadOnly(True)

        self.einzel_layout.addWidget(self.einzel_slider1)
        self.einzel_layout.addWidget(self.einzel_slider2)
        self.einzel_layout.addWidget(self.einzel_input_labels[0])
        self.einzel_layout.addWidget(self.einzel_inputs[0])
        self.einzel_layout.addWidget(self.einzel_input_labels[1])
        self.einzel_layout.addWidget(self.einzel_inputs[1])
        self.einzel_layout.addWidget(self.einzel_output_label)
        self.einzel_layout.addWidget(self.einzel_output)
        self.einzel_group.setLayout(self.einzel_layout)

        # Add the "Source Cathode" and "Einzel Extraction" sections to the horizontal layout
        self.horizontal_layout.addWidget(self.source_cathode_group)
        self.horizontal_layout.addWidget(self.einzel_group)

        # Set equal stretch for both sections to ensure equal width
        self.horizontal_layout.setStretch(0, 1)
        self.horizontal_layout.setStretch(1, 1)

        # Add the horizontal layout to the right layout
        self.right_layout.addLayout(self.horizontal_layout)

        # Add new section with specified components in a group box
        self.new_section_group = QGroupBox("New Section")
        self.new_section_layout = QVBoxLayout()

        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItems(["Option 1", "Option 2", "Option 3"])

        self.press_button = QPushButton("Press")

        self.led_layout = QHBoxLayout()
        self.led_indicators = [LEDIndicator() for _ in range(5)]
        self.led_labels = [QLabel(f"LED {i + 1}") for i in range(5)]

        for label, led in zip(self.led_labels, self.led_indicators):
            v_layout = QVBoxLayout()
            v_layout.addWidget(label)
            v_layout.addWidget(led)
            self.led_layout.addLayout(v_layout)

        self.new_input_labels = [QLabel(f"Input {i + 1}") for i in range(4)]
        self.new_inputs = [QLineEdit() for _ in range(4)]

        self.new_output_label = QLabel("Output")
        self.new_output = QTextEdit()
        self.new_output.setReadOnly(True)

        self.new_section_layout.addWidget(self.dropdown_menu)
        self.new_section_layout.addWidget(self.press_button)
        self.new_section_layout.addLayout(self.led_layout)

        for label, input_text in zip(self.new_input_labels, self.new_inputs):
            self.new_section_layout.addWidget(label)
            self.new_section_layout.addWidget(input_text)

        self.new_section_layout.addWidget(self.new_output_label)
        self.new_section_layout.addWidget(self.new_output)

        self.new_section_group.setLayout(self.new_section_layout)

        # Add the new section layout to the right layout
        self.right_layout.addWidget(self.new_section_group)

        # Add new Section 1
        self.section1_group = QGroupBox("Section 1")
        self.section1_layout = QVBoxLayout()

        # Add widgets to Section 1 as needed
        self.section1_label = QLabel("Section 1 Content")
        self.section1_layout.addWidget(self.section1_label)

        self.section1_group.setLayout(self.section1_layout)
        self.right_layout.addWidget(self.section1_group)

        # Add new Section 2
        self.section2_group = QGroupBox("Section 2")
        self.section2_layout = QVBoxLayout()

        # Add widgets to Section 2 as needed
        self.section2_label = QLabel("Section 2 Content")
        self.section2_layout.addWidget(self.section2_label)

        self.section2_group.setLayout(self.section2_layout)
        self.right_layout.addWidget(self.section2_group)

        # Add remaining widgets to the right layout
        self.right_layout.addWidget(self.data_display)
        self.right_layout.addWidget(self.stop_button)

        self.main_layout.addLayout(self.left_layout)
        self.main_layout.addLayout(self.right_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = DeviceView()
    window.show()
    sys.exit(app.exec())
┴