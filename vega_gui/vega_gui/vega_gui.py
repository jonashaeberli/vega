import sys
import threading
import rclpy
from xml.dom import Node
from python_qt_binding.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QWidget
)
from python_qt_binding.QtCore import (Qt, QTimer)
from python_qt_binding.QtXml import QDomDocument

from .main_window_ui import Ui_MainWindow
from .manage_scroll_view import ManageScrollWidgets
from .vega_gui_node import VegaGuiNode


class VegaGui(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.connectSignalsSlots()
        self.manage_scroll_widgets = ManageScrollWidgets(self.ui)

        rclpy.init(args=None)
        self.ros_node = VegaGuiNode()
        self.ros_thread = threading.Thread(target=self.run_ros_node, daemon=True)
        self.ros_thread.start()

        self.update_timer = QTimer(self)
        self.update_timer.timeout.connect(self.check_ros_data)
        self.update_timer.start(100)


    def run_ros_node(self):
        rclpy.spin(self.ros_node)
        rclpy.shutdown()

    
    def check_ros_data(self):
        # Check if the ROS node has new data
        if self.ros_node.response_data:
            print(f"Received data: {self.ros_node.response_data}")
            self.ros_node.response_data = None


    def connectSignalsSlots(self):
        self.ui.action_add_viapoint.triggered.connect(self.add_viapoint)
        self.ui.action_add_gripper.triggered.connect(self.add_gripper)

    def add_viapoint(self):
        self.manage_scroll_widgets.add_widget_set('move')
        self.ros_node.publish_message('adding via point')

    def add_gripper(self):
        self.manage_scroll_widgets.add_widget_set('gripper')

    def closeEvent(self, event):
        self.ros_node.destroy_node()
        event.accept()


def main(args=None):
    app = QApplication(sys.argv)
    win = VegaGui()
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
