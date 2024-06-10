import PyDAQmx as daq
import ctypes

class DeviceModel:
    def __init__(self):
        self.devices = []

    def refresh_daq_devices(self):
        try:
            buffer_size = 2048
            data = ctypes.create_string_buffer(buffer_size)
            daq.DAQmxGetSysDevNames(data, buffer_size)
            devices = data.value.decode('utf-8').strip().split(',')
            if not devices or devices == ['']:
                raise Exception("No DAQ devices found.")
            return devices
        except Exception as e:
            print(f"Error getting available DAQ devices: {e}")
            return []

    def get_available_channels(self, device_name):
        try:
            buffer_size = 2048
            data = ctypes.create_string_buffer(buffer_size)
            daq.DAQmxGetDevAIPhysicalChans(device_name.encode('utf-8'), data, buffer_size)
            channels = data.value.decode('utf-8').strip().split(',')
            if not channels or channels == ['']:
                raise Exception("No available channels found.")
            return channels
        except Exception as e:
            print(f"Error getting available channels for {device_name}: {e}")
            return []

    def refresh_devices(self):
        daq_devices = self.refresh_daq_devices()
        self.devices = daq_devices
        return self.devices
