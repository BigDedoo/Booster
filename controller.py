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
        self.x = {}
        self.y = {}
        self.channel_to_plot_widget = {}  # Mapping of channels to plot widgets

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
        channel = item.text()

        # Check if the channel is already selected
        if channel in self.channel_to_plot_widget:
            print(f"Channel {channel} is already selected.")
            return

        self.view.data_display.append(f"Selected channel: {channel}")

        if len(self.channel_to_plot_widget) == 0:
            self.channel_to_plot_widget[channel] = self.view.plot_widget_1
        elif len(self.channel_to_plot_widget) == 1:
            self.channel_to_plot_widget[channel] = self.view.plot_widget_2
        else:
            print("Both plot widgets are already in use.")
            return

        self.x[channel] = []
        self.y[channel] = []
        self.plot_data[channel] = PlotDataItem()
        self.channel_to_plot_widget[channel].addItem(self.plot_data[channel])

        self.start_data_acquisition(channel)

    def start_data_acquisition(self, channel):
        task = daq.Task()
        try:
            task.CreateAIVoltageChan(channel.encode('utf-8'), "", daq.DAQmx_Val_Cfg_Default, -10.0, 10.0,
                                     daq.DAQmx_Val_Volts, None)
            task.CfgSampClkTiming("", 1000, daq.DAQmx_Val_Rising, daq.DAQmx_Val_ContSamps, 1000)
            self.daq_tasks.append(task)
            thread = threading.Thread(target=self.read_data, args=(task, channel))
            thread.start()
            self.threads.append(thread)
        except Exception as e:
            task.StopTask()
            task.ClearTask()
            self.daq_tasks.remove(task)
            self.view.data_display.append(f"Error starting task for {channel}: {e}")

    def stop_data_reception(self):
        self.running = False
        for task in self.daq_tasks:
            task.StopTask()
            task.ClearTask()
        self.daq_tasks = []
        self.threads = []
        self.clear_plot()

    def clear_plot(self):
        self.view.plot_widget_1.clear()
        self.view.plot_widget_2.clear()
        self.channel_to_plot_widget.clear()
        self.plot_data.clear()
        self.x.clear()
        self.y.clear()

    def read_data(self, task, channel):
        self.running = True
        while self.running:
            data = np.zeros((1000,), dtype=np.float64)
            read = daq.int32()
            task.ReadAnalogF64(1000, 10.0, daq.DAQmx_Val_GroupByScanNumber, data, len(data), daq.byref(read), None)

            current_time = time.time()
            time_intervals = np.linspace(current_time, current_time + 1, num=1000)

            self.x[channel].extend(time_intervals.tolist())
            self.y[channel].extend(data.tolist())

            # Ensure self.x[channel] and self.y[channel] have the same length before plotting
            if len(self.x[channel]) == len(self.y[channel]):
                self.plot_data[channel].setData(self.x[channel], self.y[channel])
            else:
                print("Warning: Mismatch in length of x and y arrays")

            time.sleep(1)
