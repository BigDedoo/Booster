import sys
from PyQt6.QtWidgets import QApplication
from model import DeviceModel
from view import DeviceView
from controller import DeviceController
import qdarktheme


def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    model = DeviceModel()
    view = DeviceView()
    controller = DeviceController(model, view)

    view.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()