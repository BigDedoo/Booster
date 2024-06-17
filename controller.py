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
        self.daq_task = None
        self.thread = None
        self.plot_data = {}
        self.x = {}
        self.y = {}
        self.channels = []

        self.view.stop_button.clicked.connect(self.stop_data_reception)

        # Refresh the device list and automatically start plotting
        self.refresh_device_list()

    def refresh_device_list(self):
        devices = self.model.refresh_devices()
        if devices:
            first_device = devices[1]
            channels = self.model.get_available_channels(first_device)
            if channels:
                self.channels = channels[2:4]  # Assume we want to read from the first two channels
                self.start_plotting_channels(self.channels)

    def start_plotting_channels(self, channels):
        for channel in channels:
            self.x[channel] = []
            self.y[channel] = []
            self.plot_data[channel] = PlotDataItem()
            if channel == channels[0]:
                self.view.plot_widget_1.addItem(self.plot_data[channel])
            else:
                self.view.plot_widget_2.addItem(self.plot_data[channel])

        self.start_data_acquisition(channels)

    def start_data_acquisition(self, channels):
        self.daq_task = daq.Task()
        try:
            for channel in channels:
                self.daq_task.CreateAIVoltageChan(channel.encode('utf-8'), "", daq.DAQmx_Val_Cfg_Default, -10.0, 10.0,
                                                  daq.DAQmx_Val_Volts, None)
            self.daq_task.CfgSampClkTiming("", 1000, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 1000)
            self.thread = threading.Thread(target=self.read_data, args=(self.daq_task, channels))
            self.running = True
            self.thread.start()
        except Exception as e:
            self.daq_task.StopTask()
            self.daq_task.ClearTask()
            self.view.data_display.append(f"Error starting task for {channels}: {e}")

    def stop_data_reception(self):
        self.running = False
        if self.daq_task:
            self.daq_task.StopTask()
            self.daq_task.ClearTask()
        self.daq_task = None
        self.thread = None

    def read_data(self, task, channels):
        while self.running:
            data = np.zeros((len(channels), 1000), dtype=np.float64)
            read = daq.int32()
            task.ReadAnalogF64(1000, 10.0, daq.DAQmx_Val_GroupByChannel, data, data.size, daq.byref(read), None)

            current_time = time.time()
            time_intervals = np.linspace(current_time, current_time + 1, num=1000)

            for i, channel in enumerate(channels):
                self.x[channel].extend(time_intervals.tolist())
                self.y[channel].extend(data[i].tolist())
                # Ensure self.x[channel] and self.y[channel] have the same length before plotting
                if len(self.x[channel]) == len(self.y[channel]):
                    self.plot_data[channel].setData(self.x[channel], self.y[channel])
                else:
                    print("Warning: Mismatch in length of x and y arrays")

            time.sleep(1)
