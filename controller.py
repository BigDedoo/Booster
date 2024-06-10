import threading
import time
import PyDAQmx as daq
import numpy as np
from pyqtgraph import PlotDataItem

class DeviceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.running = False
        self.daq_tasks = []
        self.threads = []
        self.plot_data = {}
        self.x = []
        self.y = {}

        self.view.refresh_button.clicked.connect(self.refresh_device_list)
        self.view.device_list.itemClicked.connect(self.device_selected)
        self.view.stop_button.clicked.connect(self.stop_data_reception)

    def refresh_device_list(self):
        devices = self.model.refresh_devices()
        self.view.device_list.clear()
        for device in devices:
            channels = self.model.get_available_channels(device)
            for channel in channels:
                self.view.device_list.addItem(channel)  # Only add channel name

    def device_selected(self, item):
        self.stop_data_reception()  # Stop any ongoing data reception
        self.clear_plot()  # Clear the plot data
        self.x = []
        self.y = {}
        channel = item.text()
        device_channel = channel  # Use the channel directly
        if 'Dev' in device_channel:  # Check if it's a DAQ device
            try:
                self.view.data_display.append(f"Selected channel: {device_channel}")
                self.running = True
                self.y[device_channel] = []
                self.plot_data[device_channel] = PlotDataItem()
                self.view.plot_widget.addItem(self.plot_data[device_channel])
                task = daq.Task()
                try:
                    task.CreateAIVoltageChan(device_channel.encode('utf-8'), "", daq.DAQmx_Val_Cfg_Default, -10.0, 10.0, daq.DAQmx_Val_Volts, None)
                    task.CfgSampClkTiming("", 1000, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 1000)
                    self.daq_tasks.append(task)
                    thread = threading.Thread(target=self.read_from_daq, args=(task, device_channel))
                    self.threads.append(thread)
                    thread.start()
                    time.sleep(0.1)  # Adding a small delay to avoid resource conflicts
                except daq.DAQError as e:
                    self.view.data_display.append(f"DAQ error on {device_channel}: {e}")
                    if task is not None:
                        task.StopTask()
                        task.ClearTask()
            except Exception as e:
                self.view.data_display.append(f"DAQ error: {e}")

    def read_from_daq(self, task, device_channel):
        data = np.zeros((1000,), dtype=np.float64)
        while self.running:
            try:
                read = daq.int32()
                task.ReadAnalogF64(1000, 10.0, daq.DAQmx_Val_GroupByChannel, data, 1000, daq.byref(read), None)
                for value in data:
                    self.update_plot(device_channel, value)
            except daq.DAQError as e:
                self.view.data_display.append(f"DAQ read error on {device_channel}: {e}")
                break
        if task is not None:
            task.StopTask()
            task.ClearTask()

    def stop_data_reception(self):
        self.running = False
        for thread in self.threads:
            if thread.is_alive():
                thread.join()
        for task in self.daq_tasks:
            if task is not None:
                try:
                    task.StopTask()
                    task.ClearTask()
                except daq.DAQError as e:
                    self.view.data_display.append(f"Error stopping/clearing task: {e}")
        self.threads = []
        self.daq_tasks = []

    def clear_plot(self):
        self.view.plot_widget.clear()
        self.plot_data = {}

    def update_plot(self, device_channel, data):
        try:
            value = float(data)
            if len(self.x) == 0:
                self.x.append(0)
            else:
                self.x.append(self.x[-1] + 1)
            self.y[device_channel].append(value)
            self.plot_data[device_channel].setData(self.x, self.y[device_channel])
        except ValueError:
            pass
