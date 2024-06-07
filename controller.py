import threading
import serial
import pyvisa
from pyvisa import VisaIOError
from pyqtgraph import PlotDataItem
import PyDAQmx as daq
import numpy as np

class DeviceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = False
        self.serial_port = None
        self.visa_resource = None
        self.daq_task = None
        self.thread = None
        self.plot_data = PlotDataItem()
        self.x = []
        self.y = []

        self.view.plot_widget.addItem(self.plot_data)

        self.view.refresh_button.clicked.connect(self.refresh_device_list)
        self.view.device_list.itemClicked.connect(self.device_selected)
        self.view.stop_button.clicked.connect(self.stop_data_reception)

    def refresh_device_list(self):
        devices = self.model.refresh_devices()
        self.view.device_list.clear()
        for device in devices:
            self.view.device_list.addItem(device)

    def device_selected(self, item):
        self.stop_data_reception()  # Stop any ongoing data reception
        self.x = []
        self.y = []
        self.plot_data.clear()
        device = item.text()
        if 'COM' in device:  # Check if it's a COM port
            try:
                self.serial_port = serial.Serial(device, 9600, timeout=1)
                self.thread = threading.Thread(target=self.read_from_serial)
                self.running = True
                self.thread.start()
            except serial.SerialException as e:
                self.view.data_display.append(f"Serial error: {e}")
        elif 'Dev' in device:  # Check if it's a DAQ device
            try:
                channels = self.model.get_available_channels(device)
                if channels:
                    self.view.data_display.append(f"Available channels on {device}: {', '.join(channels)}")
                    # Select the first available channel for reading
                    selected_channel = channels[0]
                    self.daq_task = daq.Task()
                    self.daq_task.CreateAIVoltageChan(selected_channel.encode('utf-8'), "", daq.DAQmx_Val_Cfg_Default, -10.0, 10.0, daq.DAQmx_Val_Volts, None)
                    self.daq_task.CfgSampClkTiming("", 1000, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 1000)
                    self.data = np.zeros((1000,), dtype=np.float64)
                    self.thread = threading.Thread(target=self.read_from_daq)
                    self.running = True
                    self.thread.start()
                else:
                    self.view.data_display.append(f"No available channels found on {device}")
            except Exception as e:
                self.view.data_display.append(f"DAQ error: {e}")
        else:  # Assume it's a VISA resource
            try:
                rm = pyvisa.ResourceManager()
                resources = rm.list_resources()
                if device in resources:
                    self.visa_resource = rm.open_resource(device)
                    self.thread = threading.Thread(target=self.read_from_visa)
                    self.running = True
                    self.thread.start()
                else:
                    self.view.data_display.append(f"Device not found in available resources: {device}")
            except VisaIOError as e:
                self.view.data_display.append(f"VISA error: {e}")

    def read_from_serial(self):
        while self.running and self.serial_port.is_open:
            data = self.serial_port.readline().decode('utf-8').strip()
            if data:
                self.view.data_display.append(data)
                self.update_plot(data)
        self.serial_port.close()

    def read_from_visa(self):
        while self.running:
            try:
                data = self.visa_resource.read()
                self.view.data_display.append(data)
                self.update_plot(data)
            except VisaIOError as e:
                self.view.data_display.append(f"Error: {e}")
                break
        self.visa_resource.close()

    def read_from_daq(self):
        while self.running:
            try:
                read = daq.int32()
                self.daq_task.ReadAnalogF64(1000, 10.0, daq.DAQmx_Val_GroupByChannel, self.data, 1000, daq.byref(read), None)
                for value in self.data:
                    self.update_plot(value)
            except Exception as e:
                self.view.data_display.append(f"DAQ read error: {e}")
                break

    def stop_data_reception(self):
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join()
        if self.daq_task:
            self.daq_task.StopTask()
            self.daq_task.ClearTask()

    def update_plot(self, data):
        try:
            value = float(data)
            if len(self.x) == 0:
                self.x.append(0)
            else:
                self.x.append(self.x[-1] + 1)
            self.y.append(value)
            self.plot_data.setData(self.x, self.y)
        except ValueError:
            pass
