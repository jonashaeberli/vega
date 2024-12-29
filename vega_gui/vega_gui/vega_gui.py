import sys
from python_qt_binding.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QWidget
)
from python_qt_binding.QtCore import Qt
from python_qt_binding.QtXml import QDomDocument

from .main_window_ui import Ui_MainWindow
from .manage_scroll_view import ManageScrollWidgets


class VegaGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connectSignalsSlots()

        self.manage_scroll_widgets = ManageScrollWidgets(self.ui)


    def connectSignalsSlots(self):
        self.ui.action_add_viapoint.triggered.connect(self.add_viapoint)
        self.ui.action_export_program.triggered.connect(self.export_to_xml)
        self.ui.action_add_gripper.triggered.connect(self.add_gripper)

    def add_viapoint(self):
        self.manage_scroll_widgets.add_widget_set('move')

    def add_gripper(self):
        self.manage_scroll_widgets.add_widget_set('gripper')


    def export_to_xml(self):
        # Gather data from the model
        viapoints = self.model.getViaPoints()

        # Create XML document
        doc = QDomDocument("Viapoints")
        root = doc.createElement("viapoints")
        doc.appendChild(root)

        for i, vp in enumerate(viapoints, start=1):
            vp_element = doc.createElement("viapoint")
            vp_element.setAttribute("id", i)
            for key, value in vp.items():
                child = doc.createElement(key)
                child.appendChild(doc.createTextNode(str(value)))
                vp_element.appendChild(child)
            root.appendChild(vp_element)

        # Ask user for file name and save
        options = QFileDialog.Options()
        filename, _ = QFileDialog.getSaveFileName(self, "Save XML File", "", "XML Files (*.xml)", options=options)
        if filename:
            with open(filename, 'w') as file:
                file.write(doc.toString())


def main():
    app = QApplication(sys.argv)
    win = VegaGui()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
