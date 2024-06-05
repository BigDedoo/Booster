import serial.tools.list_ports
import pyvisa
import win32com.client

class DeviceModel:
    def __init__(self):
        self.devices = []

    def refresh_com_ports(self):
        return [port.device for port in serial.tools.list_ports.comports()]

    def refresh_ni_devices(self):
        rm = pyvisa.ResourceManager()
        ni_devices = []
        try:
            ni_devices = list(rm.list_resources())
        except Exception as e:
            print(f"Error detecting NI devices: {e}")
        return ni_devices

    def refresh_ni_pci_cards(self):
        ni_pci_cards = []
        try:
            objWMI = win32com.client.GetObject("winmgmts:\\\\.\\root\\cimv2")
            colItems = objWMI.ExecQuery("SELECT * FROM Win32_PnPEntity WHERE Manufacturer='National Instruments'")
            for item in colItems:
                ni_pci_cards.append(item.Name)
        except Exception as e:
            print(f"Error detecting NI PCI cards: {e}")
        return ni_pci_cards

    def refresh_devices(self):
        com_ports = self.refresh_com_ports()
        ni_devices = self.refresh_ni_devices()
        ni_pci_cards = self.refresh_ni_pci_cards()
        self.devices = com_ports + ni_devices + ni_pci_cards
        return self.devices