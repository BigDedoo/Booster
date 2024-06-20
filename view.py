from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTextEdit, QHBoxLayout, \
    QSlider, QLineEdit, QLabel, QComboBox, QGroupBox, QTabWidget, QGridLayout, QSizePolicy
from PyQt6.QtCore import Qt, pyqtSignal, pyqtSlot
import pyqtgraph as pg
from GraphicalElements import SliderWithText, LEDIndicator, OutputWidget

class SourceCathodeSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Source Cathode", parent)

        self.layout = QVBoxLayout()

        self.slider1 = SliderWithText("V electrode 1 (V)")
        self.slider2 = SliderWithText("I cathode (A)")
        self.input_label = QLabel("E2 (kV)")
        self.input_text = QLineEdit()

        self.layout.addWidget(self.slider1)
        self.layout.addWidget(self.slider2)
        self.layout.addWidget(self.input_label)
        self.layout.addWidget(self.input_text)
        self.setLayout(self.layout)


class EinzelExtractionSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Einzel Extraction", parent)

        self.layout = QHBoxLayout()
        self.meta_layout_left = QVBoxLayout()
        self.meta_layout_right = QGridLayout()

        self.einzel_slider1 = SliderWithText("St 120Y (A)")
        self.einzel_slider2 = SliderWithText("120° (A)")
        self.einzel_input_labels = [QLabel(f"Einzel Input {i + 1}") for i in range(2)]
        self.einzel_inputs = [QLineEdit() for _ in range(2)]

        self.einzel_output_label = QLabel("Einzel Output")
        self.einzel_output = QTextEdit()
        self.einzel_output.setReadOnly(True)

        self.meta_layout_left.addWidget(self.einzel_slider1)
        self.meta_layout_left.addWidget(self.einzel_slider2)

        self.meta_layout_right.addWidget(self.einzel_input_labels[0], 0, 0)
        self.meta_layout_right.addWidget(self.einzel_inputs[0], 0, 1)
        self.meta_layout_right.addWidget(self.einzel_input_labels[1], 1, 0)
        self.meta_layout_right.addWidget(self.einzel_inputs[1], 1, 1)
        self.meta_layout_right.addWidget(self.einzel_output_label, 2, 0)
        self.meta_layout_right.addWidget(self.einzel_output, 2, 1)

        self.layout.addLayout(self.meta_layout_left)
        self.layout.addLayout(self.meta_layout_right)

        self.setLayout(self.layout)


class LedSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("New Section", parent)

        self.layout = QHBoxLayout()
        self.meta_layout_left = QVBoxLayout()
        self.meta_layout_right = QVBoxLayout()

        self.dropdown_menu = QComboBox()
        self.dropdown_menu.addItems(["Option 1", "Option 2", "Option 3"])

        self.press_button = QPushButton("Press")

        self.led_layout = QHBoxLayout()
        self.led_indicators = [LEDIndicator() for _ in range(5)]
        self.led_labels = [QLabel("Valve 1+ T"), QLabel("CF 1+ A"), QLabel("Valve 1+ A"), QLabel("CF N+ A")]

        for label, led in zip(self.led_labels, self.led_indicators):
            v_layout = QVBoxLayout()
            v_layout.addWidget(label)
            v_layout.addWidget(led)
            self.led_layout.addLayout(v_layout)

        self.new_input_labels = [QLabel("I(1+)"), QLabel("I(N+) ON"), QLabel("I(N+) OFF"), QLabel("Charge N+")]
        self.new_inputs = [QLineEdit() for _ in range(4)]

        self.new_output_label = QLabel("Rendement")
        self.new_output = QTextEdit()
        self.new_output.setReadOnly(True)

        self.meta_layout_left.addWidget(self.dropdown_menu)
        self.meta_layout_left.addWidget(self.press_button)
        self.meta_layout_left.addLayout(self.led_layout)

        for label, input_text in zip(self.new_input_labels, self.new_inputs):
            self.meta_layout_left.addWidget(label)
            self.meta_layout_left.addWidget(input_text)

        self.meta_layout_right.addWidget(self.new_output_label)
        self.meta_layout_right.addWidget(self.new_output)

        self.layout.addLayout(self.meta_layout_left, stretch=3)
        self.layout.addLayout(self.meta_layout_right, stretch=1)

        self.setLayout(self.layout)
        # self.setMaximumHeight(500)


class Section1(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Section 1", parent)

        self.layout = QHBoxLayout()

        self.meta_layout_left = QVBoxLayout()
        self.meta_layout_right = QVBoxLayout()

        # 3 sliders with their respective text inputs
        self.slider1 = SliderWithText("90° (A)")
        self.slider2 = SliderWithText("St 90Y (V)")
        self.slider3 = SliderWithText("DeltaV (V)")

        # 2 text outputs
        self.output1_label = QLabel("Hall 90 (mT)")
        self.output1 = QTextEdit()
        self.output1.setReadOnly(True)

        self.output2_label = QLabel("Intensité 90 lue (A)")
        self.output2 = QTextEdit()
        self.output2.setReadOnly(True)

        # Adding widgets to layout
        self.meta_layout_left.addWidget(self.slider1)
        self.meta_layout_left.addWidget(self.slider2)
        self.meta_layout_left.addWidget(self.slider3)
        self.meta_layout_right.addWidget(self.output1_label)
        self.meta_layout_right.addWidget(self.output1)
        self.meta_layout_right.addWidget(self.output2_label)
        self.meta_layout_right.addWidget(self.output2)

        self.layout.addLayout(self.meta_layout_left, stretch=5)
        self.layout.addLayout(self.meta_layout_right, stretch=2)

        self.setLayout(self.layout)


class Section2(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Section 2", parent)

        self.layout = QHBoxLayout()

        self.meta_layout_left = QVBoxLayout()
        self.meta_layout_right = QGridLayout()

        # 4 sliders with their respective text inputs
        self.slider1 = SliderWithText("Gas (V)")
        self.slider2 = SliderWithText("ConfInj (A)")
        self.slider3 = SliderWithText("ConfMed (A)")
        self.slider4 = SliderWithText("ConfExt (A)")

        # 4 text outputs in a 2x2 grid
        self.output1 = OutputWidget("Output 1")
        self.output2 = OutputWidget("Output 2")
        self.output3 = OutputWidget("Output 3")
        self.output4 = OutputWidget("Pinc 14Ghz (W)")

        # One LED indicator
        self.led_label = QLabel("LED Indicator")
        self.led = LEDIndicator()

        # Adding sliders to the left layout
        self.meta_layout_left.addWidget(self.slider1)
        self.meta_layout_left.addWidget(self.slider2)
        self.meta_layout_left.addWidget(self.slider3)
        self.meta_layout_left.addWidget(self.slider4)

        # Adding output widgets to the grid layout (2x2)
        self.meta_layout_right.addWidget(self.output1, 0, 0)
        self.meta_layout_right.addWidget(self.output2, 0, 1)
        self.meta_layout_right.addWidget(self.output3, 1, 0)
        self.meta_layout_right.addWidget(self.output4, 1, 1)

        self.meta_layout_left.addWidget(self.led_label)
        self.meta_layout_left.addWidget(self.led)

        self.layout.addLayout(self.meta_layout_left, stretch=3)
        self.layout.addLayout(self.meta_layout_right, stretch=2)

        self.setLayout(self.layout)


class TabSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Tabbed Section", parent)

        self.layout = QVBoxLayout()
        self.tabs = QTabWidget()

        tab_labels = [
            "K1 rem Ana", "K1 rem RS232 SM", "K1 rem RS232 BAvg", "K1 rem RS232 MFilt",
            "K2 rem RS232 SM", "K2 Ana", "K2 rem Ana", "LN Ampli", "K RFA"
        ]

        for label in tab_labels:
            tab = QWidget()
            tab_layout = QVBoxLayout()
            tab_layout.addWidget(QLabel(f"Content of {label}"))
            tab.setLayout(tab_layout)
            self.tabs.addTab(tab, label)

        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)


class DeviceView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("COM Port and NI Devices")

        self.main_layout = QHBoxLayout()
        self.meta_layout_1 = QVBoxLayout()
        self.meta_layout_2 = QVBoxLayout()
        self.plot_layout = QVBoxLayout()
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
        self.new_section = LedSection()
        self.section1 = Section1()
        self.section2 = Section2()

        self.main_layout.addLayout(self.plot_layout)
        self.meta_layout_1.addWidget(self.source_cathode_section)
        self.meta_layout_1.addWidget(self.einzel_extraction_section)
        self.meta_layout_1.addWidget(self.section1)
        self.meta_layout_1.addWidget(self.section2)

        # Set relative size for meta_layout_1 and meta_layout_2
        self.main_layout.addLayout(self.meta_layout_1)
        self.main_layout.addLayout(self.meta_layout_2)

        self.data_layout.addWidget(self.data_display)
        self.data_layout.addWidget(self.stop_button)
        self.leds_layout.addWidget(self.new_section)

        self.tab_layout.addWidget((self.tab_section))

        self.meta_layout_2.addLayout(self.leds_layout)
        self.meta_layout_2.addLayout(self.tab_layout)
        self.main_layout.addLayout(self.meta_layout_2)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

        self.showMaximized()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = DeviceView()
    window.show()
    sys.exit(app.exec())
