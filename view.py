from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, \
    QSlider, QLineEdit, QLabel, QComboBox, QGroupBox, QTabWidget
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


class SourceCathodeSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Source Cathode", parent)

        self.layout = QVBoxLayout()

        self.slider1 = SliderWithText("Slider 1")
        self.slider2 = SliderWithText("Slider 2")
        self.input_label = QLabel("Input Text")
        self.input_text = QLineEdit()

        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.setLayout(self.layout)


class EinzelExtractionSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Einzel Extraction", parent)

        self.layout = QVBoxLayout()

        self.einzel_slider1 = SliderWithText("Einzel Slider 1")
        self.einzel_slider2 = SliderWithText("Einzel Slider 2")
        self.einzel_input_labels = [QLabel(f"Einzel Input {i + 1}") for i in range(2)]
        self.einzel_inputs = [QLineEdit() for _ in range(2)]

        self.einzel_output_label = QLabel("Einzel Output")
        self.einzel_output = QTextEdit()
        self.einzel_output.setReadOnly(True)

        self.layout.addWidget(self.einzel_slider1)
        self.layout.addWidget(self.einzel_slider2)
        self.layout.addWidget(self.einzel_input_labels[0])
        self.layout.addWidget(self.einzel_inputs[0])
        self.layout.addWidget(self.einzel_input_labels[1])
        self.layout.addWidget(self.einzel_inputs[1])
        self.layout.addWidget(self.einzel_output_label)
        self.layout.addWidget(self.einzel_output)
        self.setLayout(self.layout)


class NewSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("New Section", parent)

        self.layout = QVBoxLayout()

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

        self.layout.addWidget(self.dropdown_menu)
        self.layout.addWidget(self.press_button)
        self.layout.addLayout(self.led_layout)

        for label, input_text in zip(self.new_input_labels, self.new_inputs):
            self.layout.addWidget(label)
            self.layout.addWidget(input_text)

        self.layout.addWidget(self.new_output_label)
        self.layout.addWidget(self.new_output)

        self.setLayout(self.layout)


class Section1(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Section 1", parent)

        self.layout = QVBoxLayout()

        # 3 sliders with their respective text inputs
        self.slider1 = SliderWithText("Slider 1")
        self.slider2 = SliderWithText("Slider 2")
        self.slider3 = SliderWithText("Slider 3")

        # 2 text outputs
        self.output1_label = QLabel("Output 1")
        self.output1 = QTextEdit()
        self.output1.setReadOnly(True)

        self.output2_label = QLabel("Output 2")
        self.output2 = QTextEdit()
        self.output2.setReadOnly(True)

        # Adding widgets to layout
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.layout.addWidget(self.slider3)
        self.layout.addWidget(self.output1_label)
        self.layout.addWidget(self.output1)
        self.layout.addWidget(self.output2_label)
        self.layout.addWidget(self.output2)

        self.setLayout(self.layout)


class Section2(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Section 2", parent)

        self.layout = QVBoxLayout()

        # 4 sliders with their respective text inputs
        self.slider1 = SliderWithText("Slider 1")
        self.slider2 = SliderWithText("Slider 2")
        self.slider3 = SliderWithText("Slider 3")
        self.slider4 = SliderWithText("Slider 4")

        # 4 text outputs
        self.output1_label = QLabel("Output 1")
        self.output1 = QTextEdit()
        self.output1.setReadOnly(True)

        self.output2_label = QLabel("Output 2")
        self.output2 = QTextEdit()
        self.output2.setReadOnly(True)

        self.output3_label = QLabel("Output 3")
        self.output3 = QTextEdit()
        self.output3.setReadOnly(True)

        self.output4_label = QLabel("Output 4")
        self.output4 = QTextEdit()
        self.output4.setReadOnly(True)

        # One LED indicator
        self.led_label = QLabel("LED Indicator")
        self.led = LEDIndicator()

        # Adding widgets to layout
        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.layout.addWidget(self.slider3)
        self.layout.addWidget(self.slider4)
        self.layout.addWidget(self.output1_label)
        self.layout.addWidget(self.output1)
        self.layout.addWidget(self.output2_label)
        self.layout.addWidget(self.output2)
        self.layout.addWidget(self.output3_label)
        self.layout.addWidget(self.output3)
        self.layout.addWidget(self.output4_label)
        self.layout.addWidget(self.output4)
        self.layout.addWidget(self.led_label)
        self.layout.addWidget(self.led)

        self.setLayout(self.layout)

class TabSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Tabbed Section", parent)

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()

        for i in range(1, 10):
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(QLabel(f"Content of Tab {i}"))
            tab.setLayout(tab_layout)
            self.tabs.addTab(tab, f"Tab {i}")

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

class DeviceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port and NI Devices")

        self.main_layout = QHBoxLayout()
        self.plot_layout = QVBoxLayout()
        self.main_layout = QHBoxLayout()
        self.data_layout = QVBoxLayout()
        self.leds_layout = QVBoxLayout()
        self.tab_layout = QVBoxLayout()

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

        self.plot_layout.addWidget(self.plot_widget_1)
        self.plot_layout.addWidget(self.plot_widget_2)

        self.source_cathode_section = SourceCathodeSection()
        self.einzel_extraction_section = EinzelExtractionSection()
        self.tab_section = TabSection()
        self.new_section = NewSection()
        self.section1 = Section1()
        self.section2 = Section2()

        self.main_layout.addLayout(self.plot_layout)
        self.main_layout.addWidget(self.source_cathode_section)
        self.main_layout.addWidget(self.einzel_extraction_section)
        self.main_layout.addWidget(self.section1)
        self.main_layout.addWidget(self.section2)

        self.data_layout.addWidget(self.data_display)
        self.data_layout.addWidget(self.stop_button)

        self.leds_layout.addWidget(self.new_section)

        self.tab_layout.addWidget((self.tab_section))

        self.main_layout.addLayout(self.main_layout)
        self.main_layout.addLayout(self.leds_layout)
        self.main_layout.addLayout(self.data_layout)
        self.main_layout.addLayout(self.tab_layout)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = DeviceView()
    window.show()
    sys.exit(app.exec())
