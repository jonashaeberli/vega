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
from vega_kinematics_solver.kinematics import Kinematics


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
        self.ui.check_box_show_interactive_marker.stateChanged.connect(self.handle_checkbox_state_change)
        self.ui.calculate_trajectory_btn.clicked.connect(self.calculate_trajectory)

    def add_viapoint(self):
        self.manage_scroll_widgets.add_widget_set('move')

    def add_gripper(self):
        self.manage_scroll_widgets.add_widget_set('gripper')

    def handle_checkbox_state_change(self, state):
        # Handle when checkbox is checked or unchecked
        if state == 2:  # Qt.Checked
            print("Checkbox is checked")
            self.show_interactive_marker()  # Call function for checked state
        else:  # Qt.Unchecked or Qt.PartiallyChecked
            print("Checkbox is unchecked")
            self.hide_interactive_marker()  # Call function for unchecked state    

    def show_interactive_marker(self):
        self.ros_node.create_interactive_marker()

    def hide_interactive_marker(self):
        self.ros_node.cleanup_interactive_marker()

    def calculate_trajectory(self):
        (x, y, z) = self.manage_scroll_widgets.return_widget_data()
        self.ros_node.get_logger().info(f'x: {x}, y: {y}, z: {z}')
        self.ros_node.send_trajectory_planing_goal(x, y, z)

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
