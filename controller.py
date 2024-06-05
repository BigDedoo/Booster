class DeviceController:
    def __init__(self, model, view):
        self.model = model
        self.view = view
        self.view.refresh_button.clicked.connect(self.refresh_device_list)

    def refresh_device_list(self):
        devices = self.model.refresh_devices()
        self.view.device_list.clear()
        self.view.device_list.addItems(devices)