import sys
from python_qt_binding.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QInputDialog, QListWidgetItem, QFileDialog
)
from python_qt_binding.QtCore import Qt  # Import Qt from QtCore for access to Qt flags and enums
from python_qt_binding.QtXml import QDomDocument

from .main_window_ui import Ui_MainWindow
from .add_via_dialog_ui import Ui_add_via


class VegaGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connectSignalsSlots()


    def connectSignalsSlots(self):
        self.ui.action_add_viapoint.triggered.connect(self.add_viapoint)
        self.ui.action_export_program.triggered.connect(self.export_to_xml)
        self.ui.listWidget.itemDoubleClicked.connect(self.edit_viapoint)  # Connect double-click to editing



    def add_viapoint(self):
        # Create a dialog instance and set up the UI
        dialog = QDialog(self)
        ui = Ui_add_via()
        ui.setupUi(dialog)
        
        # Show the dialog and check if the user clicked 'Ok'
        if dialog.exec_() == QDialog.Accepted:
            # Retrieve the values from the spin boxes
            x = ui.doubleSpinBox.value()
            y = ui.doubleSpinBox_2.value()
            z = ui.doubleSpinBox_3.value()
            yaw = ui.doubleSpinBox_4.value()

            # Create the viapoint dictionary
            viapoint = {
                "x": x,
                "y": y,
                "z": z,
                "yaw": yaw,
                "velocity": 0,  # Or any value for velocity you need
            }

            # Create a list item with the entered data
            item = QListWidgetItem(f"X: {viapoint['x']}, Y: {viapoint['y']}, "
                                f"Z: {viapoint['z']}, Yaw: {viapoint['yaw']}, "
                                f"Velocity: {viapoint['velocity']}")
            item.setData(1, viapoint)  # Store the viapoint data in the item
            
            # Make the item editable
            item.setFlags(item.flags() | Qt.ItemIsEditable)
            
            self.ui.listWidget.addItem(item)


    def edit_viapoint(self, item):
        # When the item is double-clicked, open the dialog to edit values
        viapoint = item.data(1)  # Retrieve the stored viapoint data
        
        # Create a dialog instance and set up the UI
        dialog = QDialog(self)
        ui = Ui_add_via()
        ui.setupUi(dialog)
        
        # Set the current values in the dialog
        ui.doubleSpinBox.setValue(viapoint["x"])
        ui.doubleSpinBox_2.setValue(viapoint["y"])
        ui.doubleSpinBox_3.setValue(viapoint["z"])
        ui.doubleSpinBox_4.setValue(viapoint["yaw"])

        # Connect the Cancel button to a method that deletes the item
        dialog.rejected.connect(lambda: self.delete_viapoint(item, dialog))
        
        # Show the dialog and check if the user clicked 'Ok'
        if dialog.exec_() == QDialog.Accepted:
            # Retrieve the updated values
            viapoint["x"] = ui.doubleSpinBox.value()
            viapoint["y"] = ui.doubleSpinBox_2.value()
            viapoint["z"] = ui.doubleSpinBox_3.value()
            viapoint["yaw"] = ui.doubleSpinBox_4.value()

            # Update the text of the item
            item.setText(f"X: {viapoint['x']}, Y: {viapoint['y']}, "
                         f"Z: {viapoint['z']}, Yaw: {viapoint['yaw']}, "
                         f"Velocity: {viapoint['velocity']}")

            # Update the stored data in the item
            item.setData(1, viapoint)

    def delete_viapoint(self, item, dialog):
        # Delete the item from the list widget and close the dialog
        row = self.ui.listWidget.row(item)  # Get the index of the item
        self.ui.listWidget.takeItem(row)  # Remove the item from the list
        dialog.accept()  # Close the dialog

    def export_to_xml(self):
        # Gather data from the list
        viapoints = []
        for i in range(self.ui.listWidget.count()):
            item = self.ui.listWidget.item(i)
            viapoints.append(item.data(1))  # Retrieve the viapoint data

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
