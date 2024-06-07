import threading
import serial
import pyvisa
from pyvisa import VisaIOError


class DeviceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = False
        self.serial_port = None
        self.visa_resource = None
        self.thread = None

        self.view.refresh_button.clicked.connect(self.refresh_device_list)
        self.view.device_list.itemClicked.connect(self.device_selected)
        self.view.stop_button.clicked.connect(self.stop_data_reception)

    def refresh_device_list(self):
        devices = self.model.refresh_devices()
        self.view.device_list.clear()
        self.view.device_list.addItems(devices)

    def device_selected(self, item):
        self.stop_data_reception()  # Stop any ongoing data reception
        device = item.text()
        if 'COM' in device:  # Check if it's a COM port
            try:
                self.serial_port = serial.Serial(device, 9600, timeout=1)
                self.thread = threading.Thread(target=self.read_from_serial)
                self.running = True
                self.thread.start()
            except serial.SerialException as e:
                self.view.data_display.append(f"Serial error: {e}")
        else:
            try:
                rm = pyvisa.ResourceManager()
                self.visa_resource = rm.open_resource(device)
                self.thread = threading.Thread(target=self.read_from_visa)
                self.running = True
                self.thread.start()
            except VisaIOError as e:
                self.view.data_display.append(f"VISA error: {e}")

    def read_from_serial(self):
        while self.running and self.serial_port.is_open:
            data = self.serial_port.readline().decode('utf-8').strip()
            if data:
                self.view.data_display.append(data)
        self.serial_port.close()

    def read_from_visa(self):
        while self.running:
            try:
                data = self.visa_resource.read()
                self.view.data_display.append(data)
            except VisaIOError as e:
                self.view.data_display.append(f"Error: {e}")
                break
        self.visa_resource.close()

    def stop_data_reception(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()