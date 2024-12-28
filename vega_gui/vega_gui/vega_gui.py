import sys
from python_qt_binding.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox
)
from .main_window_ui import Ui_MainWindow


class VegaGui(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)
        self.connectSignalsSlots()

    def connectSignalsSlots(self):
        pass

def main():
    app = QApplication(sys.argv)
    win = VegaGui()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
